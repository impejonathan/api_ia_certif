import pandas as pd 


import os
from dotenv import load_dotenv
import pyodbc

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression 
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import r2_score , mean_squared_error, mean_absolute_error
import pickle

import mlflow
import mlflow.sklearn
import os
os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5000'




def Model():
    """
    ENGLISH:
    This function loads the environment variables, connects to the SQL Server database, and retrieves data from the 'Produit', 'Caracteristiques', and 'Dimensions' tables.
    It then merges these dataframes and prepares the data for model training. The function also converts categorical columns into numerical values.
    The data is split into training and test sets, and a RandomForestRegressor model is trained on the training data.
    The function makes predictions on both the training and test data, calculates the R2 score, mean squared error (MSE), and mean absolute error (MAE) for both sets of data.
    These metrics are logged in MLflow, and the model is saved in MLflow and as a pickle file.

    FRENCH:
    Cette fonction charge les variables d'environnement, se connecte à la base de données SQL Server et récupère les données des tables 'Produit', 'Caracteristiques' et 'Dimensions'.
    Elle fusionne ensuite ces dataframes et prépare les données pour l'entraînement du modèle. La fonction convertit également les colonnes catégorielles en valeurs numériques.
    Les données sont divisées en ensembles d'entraînement et de test, et un modèle RandomForestRegressor est entraîné sur les données d'entraînement.
    La fonction fait des prédictions sur les données d'entraînement et de test, calcule le score R2, l'erreur quadratique moyenne (MSE) et l'erreur absolue moyenne (MAE) pour les deux ensembles de données.
    Ces métriques sont enregistrées dans MLflow, et le modèle est sauvegardé dans MLflow et sous forme de fichier pickle.

    """
    # Charger les variables d'environnement
    load_dotenv()

    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_DATABASE')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')

    driver= '{ODBC Driver 17 for SQL Server}'

    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()


    # Créer un DataFrame pour chaque table
    df_produit = pd.read_sql_query('SELECT * FROM Produit', cnxn)
    df_caracteristiques = pd.read_sql_query('SELECT * FROM Caracteristiques', cnxn)
    df_dimensions = pd.read_sql_query('SELECT * FROM Dimensions', cnxn)

    # Fermer la connexion
    cnxn.close()


    # Fusionner df_produit et df_caracteristiques sur 'ID_Produit'
    df = pd.merge(df_produit, df_caracteristiques, on='ID_Produit')

    # Fusionner le DataFrame résultant avec df_dimensions sur 'ID_Produit'
    df = pd.merge(df, df_dimensions, on='ID_Produit')





        # Préparer les données pour l'entraînement
    X = df.drop(columns=['Prix','URL_Produit','Info_generale','Date_scrap','ID_Caracteristique','ID_Dimension','ID_Produit'])
    y = df['Prix']

    # Convertir les colonnes catégorielles en valeurs numériques
    for col in X.select_dtypes(include=['object']).columns:
        X[col] = X[col].astype('category').cat.codes

    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Créer et entraîner le modèle
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Faire des prédictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    # Calculer le score R2
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = r2_score(y_test, y_pred_test)

    mean_squared_error_train = mean_squared_error(y_train, y_pred_train)
    mean_squared_error_test = mean_squared_error(y_test, y_pred_test)

    mean_absolute_error_train = mean_absolute_error(y_train, y_pred_train)
    mean_absolute_error_test = mean_absolute_error(y_test, y_pred_test)

    # Log metrics in MLflow
    mlflow.log_metric("r2_train", r2_train)
    mlflow.log_metric("r2_test", r2_test)
    mlflow.log_metric("mse_train", mean_squared_error_train)
    mlflow.log_metric("mse_test", mean_squared_error_test)
    mlflow.log_metric("mae_train", mean_absolute_error_train)
    mlflow.log_metric("mae_test", mean_absolute_error_test)
    
    # Sauvegarder le modèle dans MLflow
    mlflow.sklearn.log_model(model, "model")

    print(f"Le score R2 du modèle sur les données d'entraînement est : {r2_train}")
    print(f"Le score R2 du modèle sur les données de test est : {r2_test}")
    print("------------------------------")
    print(f"Le score MSE du modèle sur les données d'entraînement est : {mean_squared_error_train}")
    print(f"Le score MSE du modèle sur les données de test est : {mean_squared_error_test}")
    print("------------------------------")
    print(f"Le score MAE du modèle sur les données d'entraînement est : {mean_absolute_error_train}")
    print(f"Le score MAE du modèle sur les données de test est : {mean_absolute_error_test}")


        
    # Sauvegarder le modèle dans un fichier pickle
    with open('model.pkl', 'wb') as file:
        pickle.dump(model, file)

    print("Le modèle a été sauvegardé dans le fichier 'model.pkl'.")


    return r2_train, r2_test
# Appeler la fonction pour exécuter le code
Model()