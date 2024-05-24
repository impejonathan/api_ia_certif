# import pickle
# import pandas as pd
# import os

# os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5000'

# import mlflow
# import mlflow.sklearn
# import pandas as pd

# def predict(nouveau_produit):
#     """
#     (FR) Cette fonction prédit la sortie d'un nouveau produit en utilisant le dernier modèle généré dans MLflow.
#     Assurez-vous que le serveur MLflow est en cours d'exécution en même temps que FastAPI pour récupérer le dernier modèle généré.
#     dans le cas ou  le serveur MLflow est PAS en cours d'exécution en même temps que FastAPI pour récupérer le dernier modèle
#     généré il y a un pickel de secour du 1er model crée a la racine du code .
    
#     Args:
#         nouveau_produit (dict): Un dictionnaire contenant les caractéristiques du nouveau produit.

#     Returns:
#         prediction[0] : La prédiction du modèle pour le nouveau produit.

#     (EN) This function predicts the output of a new product using the latest model generated in MLflow.
#     Ensure that the MLflow server is running at the same time as FastAPI to retrieve the latest generated model.
    
#     Args:
#         nouveau_produit (dict): A dictionary containing the features of the new product.

#     Returns:
#         prediction[0] : The model's prediction for the new product.
#     """
    
    
#      # Initialiser le modèle à None
#     model = None

#     # Essayer de charger le dernier modèle de MLflow
#     try:
#         runs = mlflow.search_runs()
#         last_run = runs.loc[runs['start_time'].idxmax()]
#         model_uri = f"runs:/{last_run.run_id}/model"
#         model = mlflow.sklearn.load_model(model_uri)
#     except Exception as e:
#         print(f"Erreur lors du chargement du modèle de MLflow : {e}")
    
#     # Si le chargement du modèle de MLflow a échoué, charger le modèle à partir du fichier pickle
#     if model is None:
#         with open('model.pkl', 'rb') as f:
#             model = pickle.load(f)

#     # Convertir le dictionnaire en dataframe
#     df = pd.DataFrame([nouveau_produit])

#     # Convertir les colonnes catégorielles en valeurs numériques
#     for col in df.select_dtypes(include=['object']).columns:
#         df[col] = df[col].astype('category').cat.codes

#     # Faire une prédiction
#     prediction = model.predict(df)

#     return round(prediction[0], 2)



