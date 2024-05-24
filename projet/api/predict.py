import pickle
import pandas as pd
import os
import pyodbc
from dotenv import load_dotenv

import mlflow
import mlflow.sklearn
import pandas as pd


# Charger les variables d'environnement
load_dotenv()

# Informations de connexion à la base de données
server = os.environ.get('DB_SERVER')
database = os.environ.get('DB_DATABASE')
username = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')
driver = '{ODBC Driver 17 for SQL Server}'

def predict(nouveau_produit):
    """
    Cette fonction prédit la sortie d'un nouveau produit en utilisant le dernier modèle généré dans MLflow.
    Assurez-vous que le serveur MLflow est en cours d'exécution en même temps que FastAPI pour récupérer le dernier modèle généré.
    Si le serveur MLflow n'est PAS en cours d'exécution, le modèle de secours (pickle) est utilisé.

    Args:
        nouveau_produit (dict): Un dictionnaire contenant les caractéristiques du nouveau produit.

    Returns:
        prediction[0] : La prédiction du modèle pour le nouveau produit.
    """
    # try:
    #     # Charger le modèle depuis le dossier
    #     model_path = os.path.join(os.path.dirname(__file__), '..','model', 'mlarticats', '0')
    #     # Obtenir la liste des sous-dossiers
    #     subdirs = os.listdir(model_path)
    #     # Trier la liste et sélectionner le dernier élément
    #     subdir = sorted(subdirs)[-1]
    #     # Charger le modèle
    #     with open(os.path.join(model_path, subdir, 'model.pkl'), 'rb') as f:
    #         model = pickle.load(f)
    # except Exception as e:
    #     print(f"Erreur lors du chargement du modèle de MLflow : {e}")
    #     # Si le chargement du modèle de MLflow a échoué, charger le modèle à partir du fichier pickle
    #     pickle_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    #     with open(pickle_path, 'rb') as f:
    #         model = pickle.load(f)
    
    
    try:
        # Charger le modèle à partir du fichier pickle
        pickle_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
        with open(pickle_path, 'rb') as f:
            model = pickle.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement du modèle à partir du fichier pickle : {e}")
        return None


    # Convertir le dictionnaire en dataframe
    df = pd.DataFrame([nouveau_produit])

    # Convertir les colonnes catégorielles en valeurs numériques
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype('category').cat.codes

    # Faire une prédiction
    prediction = model.predict(df)[0]

    # Enregistrer la prédiction dans la table "Prediction" de la base de données
    try:
        cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = cnxn.cursor()

        # Insérer la prédiction dans la table
        cursor.execute("""
        INSERT INTO Prediction (Prix_prediction, Date_prediction, Descriptif, Note, Marque, Consommation, Indice_Pluie , Bruit , Saisonalite  , 
        Type_Vehicule , Runflat , Largeur , Hauteur , Diametre , Charge , Vitesse )
        VALUES (?, GETDATE(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, prediction, nouveau_produit['Descriptif'], nouveau_produit['Note'], nouveau_produit['Marque'], nouveau_produit['Consommation'], 
        nouveau_produit['Indice_Pluie'], nouveau_produit['Bruit'], nouveau_produit['Saisonalite'], nouveau_produit['Type_Vehicule'], nouveau_produit['Runflat'], 
        nouveau_produit['Largeur'], nouveau_produit['Hauteur'], nouveau_produit['Diametre'], nouveau_produit['Charge'], nouveau_produit['Vitesse'])

        cnxn.commit()
        cnxn.close()
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de la prédiction dans la base de données : {e}")

    return round(prediction, 2)