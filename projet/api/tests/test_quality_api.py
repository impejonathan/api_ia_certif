import pytest
import pyodbc
import os
from dotenv import load_dotenv
import pandas as pd
import pickle
import requests




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


def test_prediction_without_token():
    """
    Teste si une prédiction est refusée lorsque l'utilisateur n'est pas authentifié avec un token.
    """
    # Définir l'URL de l'API
    url = "http://localhost:8000/predict/"

    # Définir un exemple d'entrée
    item = {
  "Descriptif": "MILESTONE GREENSPORT",
  "Note": "3",
  "Marque": "MILESTONE",
  "Consommation": "D",
  "Indice_Pluie": "B",
  "Bruit": 70,
  "Saisonalite": "Été",
  "Type_Vehicule": "Tourisme",
  "Runflat": "Non",
  "Largeur": 175,
  "Hauteur": 55,
  "Diametre": 15,
  "Charge": 77,
  "Vitesse": "T"
}

    # Faire une requête POST sans token
    response = requests.post(url, json=item)

    # Vérifier que la réponse a un statut 403 (non autorisé)
    assert response.status_code == 403, "La prédiction n'a pas été refusée sans token"
    
    
    

def test_prediction_with_token():
    """
    Teste si une prédiction est réussie lorsque l'utilisateur est authentifié avec un token.
    """
    # Définir l'URL de l'API
    url = "http://localhost:8000/predict/"

    # Définir un exemple d'entrée
    item = {
      "Descriptif": "MILESTONE GREENSPORT",
      "Note": "3",
      "Marque": "MILESTONE",
      "Consommation": "D",
      "Indice_Pluie": "B",
      "Bruit": 70,
      "Saisonalite": "Été",
      "Type_Vehicule": "Tourisme",
      "Runflat": "Non",
      "Largeur": 175,
      "Hauteur": 55,
      "Diametre": 15,
      "Charge": 77,
      "Vitesse": "T"
    }

    # Définir le token d'authentification
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiJ9.o8cW7VkTdM2lVrPV0cNcskJLGBCvoQA4sxec-RusCIg"

    # Définir les headers de la requête
    headers = {"Authorization": f"Bearer {token}"}

    # Faire une requête POST avec le token
    response = requests.post(url, json=item, headers=headers)

    # Vérifier que la réponse a un statut 200 (OK)
    assert response.status_code == 200, "La prédiction a échoué avec le token"

    # Vérifier que la réponse contient une prédiction
    assert "prediction" in response.json(), "La réponse ne contient pas de prédiction"

# Exécutez le test
test_prediction_with_token()
