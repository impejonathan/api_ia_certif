import streamlit as st
import mlflow
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv
import pyodbc
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression 
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import r2_score , mean_squared_error, mean_absolute_error

# Configuration de l'URI de suivi MLflow
mlflow.set_tracking_uri("http://localhost:5000")

# Récupérer les informations du modèle le plus récent
latest_run = mlflow.search_runs(order_by=["start_time desc"]).iloc[0]
r2_train = latest_run["metrics.r2_train"]
r2_test = latest_run["metrics.r2_test"]
mse_train = latest_run["metrics.mse_train"]
mse_test = latest_run["metrics.mse_test"]
mae_train = latest_run["metrics.mae_train"]
mae_test = latest_run["metrics.mae_test"]

# Créer un DataFrame pour les scores
scores_df = pd.DataFrame({
    "Score": ["R2 (entraînement)", "R2 (test)", "MSE (entraînement)", "MSE (test)", "MAE (entraînement)", "MAE (test)"],
    "Valeur": [r2_train, r2_test, mse_train, mse_test, mae_train, mae_test]
})

# Créer trois graphiques séparés pour chaque métrique
plt.figure(figsize=(10, 6))

# Graphique R2
plt.subplot(3, 1, 1)
sns.barplot(x="Score", y="Valeur", data=scores_df[scores_df["Score"].str.contains("R2")], palette="viridis")
plt.title("R2 du modèle MLflow")
plt.xlabel("Score")
plt.ylabel("Valeur")

# Graphique MSE
plt.subplot(3, 1, 2)
sns.barplot(x="Score", y="Valeur", data=scores_df[scores_df["Score"].str.contains("MSE")], palette="viridis")
plt.title("MSE du modèle MLflow")
plt.xlabel("Score")
plt.ylabel("Valeur")

# Graphique MAE
plt.subplot(3, 1, 3)
sns.barplot(x="Score", y="Valeur", data=scores_df[scores_df["Score"].str.contains("MAE")], palette="viridis")
plt.title("MAE du modèle MLflow")
plt.xlabel("Score")
plt.ylabel("Valeur")

st.pyplot(plt)

# Afficher les scores dans Streamlit
st.title("Tableau de bord du modèle MLflow")
st.write("Scores du modèle le plus récent :")
st.dataframe(scores_df)





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





# Sélectionnez la variable explicative que vous souhaitez visualiser
selected_feature = st.selectbox("Sélectionnez une variable explicative", X_train.columns)

# Créez le premier sous-graphique pour la distribution de la variable explicative
plt.figure(figsize=(8, 6))
sns.histplot(X_train[selected_feature], bins=20, kde=True, color="skyblue")
plt.title(f"Distribution de {selected_feature}")
plt.xlabel(selected_feature)
plt.ylabel("Fréquence")
st.pyplot(plt)

# Créez le deuxième sous-graphique pour la distribution de la même variable dans l'ensemble d'entraînement
plt.figure(figsize=(8, 6))
sns.histplot(X_train[selected_feature], bins=20, kde=True, color="salmon")
plt.title(f"Distribution de {selected_feature} (Ensemble d'entraînement)")
plt.xlabel(selected_feature)
plt.ylabel("Fréquence")
st.pyplot(plt)