import pandas as pd 

import os
from dotenv import load_dotenv
import pyodbc

import pyodbc

def clean_data():
    
    """
    ENGLISH:
    This function connects to a SQL Server database using the connection details stored in environment variables.
    It then reads data from the 'Produit' table and deletes rows with 
    'Prix' = 666 from the 'Produit', 'Caracteristiques', and 'Dimensions' tables.
    
    FRENCH:
    Cette fonction se connecte à une base de données SQL Server en utilisant les détails de connexion s
    tockés dans les variables d'environnement.
    Elle lit ensuite les données de la table 'Produit' et supprime les lignes avec 
    'Prix' = 666 des tables 'Produit', 'Caracteristiques' et 'Dimensions'.

    Returns:
    None
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
        
        print("connexion établie")
    except Exception as e:
        print("connexion échouée")
        print("Erreur :", str(e))



        # Supprimer les lignes correspondantes dans la table Caracteristiques
    cursor.execute("""
        DELETE FROM Caracteristiques
        WHERE ID_Produit IN (
            SELECT ID_Produit
            FROM Produit
            WHERE Prix = 666
        )
        """)
        
        # Supprimer les lignes correspondantes dans la table Dimensions
    cursor.execute("""
        DELETE FROM Dimensions
        WHERE ID_Produit IN (
            SELECT ID_Produit
            FROM Produit
            WHERE Prix = 666
        )
        """)
        
        # Maintenant, vous pouvez supprimer les lignes de la table Produit
    cursor.execute("""
        DELETE FROM Produit
        WHERE Prix = 666
        """)
        
        # Valider les modifications
    cnxn.commit()
        
    print("Les lignes avec 'Prix' = 666 ont été supprimées.")
    
# Appeler la fonction pour exécuter le code
clean_data()