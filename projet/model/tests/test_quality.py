import pytest
import pyodbc
import os
from dotenv import load_dotenv
from ..clean import clean_data 
from ..Model import Model
import pandas as pd
import pickle

def test_database_connection():
    """
    Teste la connexion à la base de données SQL Server.
    """
    # Charger les variables d'environnement
    load_dotenv()

    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_DATABASE')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')

    driver= '{ODBC Driver 17 for SQL Server}'

    try:
        cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        
        # Essayez de lire les données de la table 'Produit'
        cursor.execute("SELECT TOP 1 * FROM Produit")
        row = cursor.fetchone()
        
        assert row is not None, "La connexion à la base de données a échoué"
    except Exception as e:
        pytest.fail(f"Erreur lors de la connexion à la base de données : {str(e)}")

# Exécutez le test
test_database_connection()


def test_delete_price_666():
    """
    Teste la suppression des lignes avec 'Prix' = 666.
    """
    # Charger les variables d'environnement
    load_dotenv()

    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_DATABASE')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')

    driver= '{ODBC Driver 17 for SQL Server}'

    try:
        cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        
        # Exécutez la fonction clean_data pour supprimer les lignes avec 'Prix' = 666
        clean_data()
        
        # Vérifiez si les lignes avec 'Prix' = 666 ont été supprimées
        cursor.execute("SELECT * FROM Produit WHERE Prix = 666")
        rows = cursor.fetchall()
        
        assert len(rows) == 0, "Les lignes avec 'Prix' = 666 n'ont pas été supprimées"
    except Exception as e:
        pytest.fail(f"Erreur lors de la suppression des lignes avec 'Prix' = 666 : {str(e)}")

# Exécutez le test
test_delete_price_666()



def test_model_r2_score():
    """
    Teste le score R2 du modèle sur les données de test.
    """
    # Exécutez la fonction Model pour entraîner le modèle et obtenir le score R2
    r2_train, r2_test = Model()

    # Vérifiez si le score R2 sur les données de test est supérieur à 0.40
    assert r2_test > 0.40, "Le score R2 du modèle sur les données de test est inférieur à 0.40"

# Exécutez le test avec pytest
pytest.main(["-k", "test_model_r2_score"])



def test_model_overfitting():
    """
    Teste si le modèle est surajusté.
    """
    # Exécutez la fonction Model pour entraîner le modèle et obtenir le score R2
    r2_train, r2_test = Model()

    # Vérifiez si la différence entre le score R2 sur les données d'entraînement et de test est inférieure à 0.20
    assert abs(r2_train - r2_test) < 0.20, "Le modèle est surajusté"

# Exécutez le test avec pytest
pytest.main(["-k", "test_model_overfitting"])




def test_model_prediction():
    """
    Teste si la prédiction du modèle est dans la plage attendue.
    """
    # Charger le modèle à partir du fichier pickle
    pickle_path = os.path.join(os.path.dirname(__file__), '..', 'model.pkl')
    with open(pickle_path, 'rb') as f:
        model = pickle.load(f)

    # Définir un nouveau produit
    nouveau_produit = {
        'Descriptif': 'MILESTONE GREENSPORT',
        'Note': '3',
        'Marque': 'MILESTONE',
        'Consommation': 'D',
        'Indice_Pluie': 'B',
        'Bruit': 70,
        'Saisonalite': 'Été',
        'Type_Vehicule': 'Tourisme',
        'Runflat': 'Non',
        'Largeur': 175,
        'Hauteur': 55,
        'Diametre': 15,
        'Charge': 77,
        'Vitesse': 'T'
    }

    # Convertir le dictionnaire en dataframe
    df_nouveau_produit = pd.DataFrame([nouveau_produit])

    # Convertir les colonnes catégorielles en valeurs numériques
    for col in df_nouveau_produit.select_dtypes(include=['object']).columns:
        df_nouveau_produit[col] = df_nouveau_produit[col].astype('category').cat.codes

    # Faire une prédiction avec le modèle
    prix_pred = model.predict(df_nouveau_produit)

    # Vérifiez si la prédiction est dans la plage attendue
    assert 0 <= prix_pred[0] <= 600, "La prédiction du modèle est en dehors de la plage attendue"

# Exécutez le test avec pytest
pytest.main(["-k", "test_model_prediction"])
