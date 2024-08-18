# Projet de Prédiction des Prix de Pneus

Ce projet vise à développer un modèle de prédiction des prix de pneus basé sur les données de Carter Cash, et à le déployer via une API sur une plateforme cloud comme Azure.

## Structure du Projet

Le projet est organisé en plusieurs dossiers principaux :

- `model/` : Contient le code pour le Machine Learning
- `ml_ops/` : Contient les scripts et configurations pour MLOps
- `api/` : Contient le code de l'API IA
- `.github/` : Contient les workflows pour CI/CD

## Prérequis

- Python 3.x
- Un environnement virtuel (`python -m venv env`)
- Les dépendances listées dans `requirements.txt`

## Configuration

1. Clonez le repository :
   ```
   git clone https://github.com/impejonathan/api_ia_certif.git
   ```

2. Créez et activez l'environnement virtuel :
   ```
   python -m venv env
   source env/bin/activate  # Sur Windows, utilisez `env\Scripts\activate`
   ```

3. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

4. Configurez les variables d'environnement en créant un fichier `.env` à la racine du projet avec le contenu suivant :
   ```
   DB_SERVER=xxxxxxx
   DB_DATABASE=xxxxxxx
   DB_USERNAME=xxxxxxx
   DB_PASSWORD=xxxxxxx
   SECRET_KEY=xxxxxxx
   token=xxxxxxx
   ```

## Étapes du Projet

1. **Collecte et Préparation des Données**
   - Connexion à la base de données Carter Cash
   - Extraction des caractéristiques et des prix des pneus

2. **Développement du Modèle (dossier `model/`)**
   - Prétraitement des données
   - Sélection et entraînement du modèle de Machine Learning
   - Évaluation et optimisation du modèle

3. **MLOps (dossier `mlops/`)**
   - Mise en place du versioning du modèle
   - Configuration du suivi des expériences
   - Automatisation du processus d'entraînement et de déploiement

4. **Développement de l'API (dossier `api/`)**
   - Création d'une API Flask ou FastAPI
   - Intégration du modèle entraîné dans l'API
   - Implémentation des endpoints pour les prédictions

5. **CI/CD (dossier `.github/`)**
   - Configuration des workflows GitHub Actions
   - Automatisation des tests, du build et du déploiement

6. **Déploiement**
   - Déploiement de l'API sur une plateforme cloud (ex: Azure)
   - Configuration des ressources cloud nécessaires


## Licence

MIT



## Étape 1 : Création et Archivage du Modèle

Cette étape consiste à créer un modèle de prédiction de prix de pneus en utilisant les données extraites de la base de données, puis à l'archiver dans MLflow pour suivre ses performances et versions. Les tests préalables peuvent être effectués dans le notebook `model.ipynb` avant de passer au script final `Model.py`.

### Contenu du Dossier `model/`

- **`main.py` :** Ce script permet de lancer les processus de nettoyage des données et de création du modèle en une seule commande depuis la racine du projet. 
- **`Model.py` :** Ce script contient le code pour la création du modèle de machine learning, son entraînement, et son archivage dans MLflow.
- **`clean.py` :** Ce script nettoie les données de la base de données en supprimant les lignes ayant des valeurs de prix spécifiques (e.g., 666).
- **`model.ipynb` :** Ce notebook Jupyter permet de tester et de prototyper le modèle avant de passer à la version scriptée.

### Contenu du Dossier `model/test`
- **`test_quality.py` :** Ce script de test, utilisant `pytest`, permet de vérifier la qualité de la connexion à la base de données, la suppression correcte des données indésirables, et la performance du modèle.

### Comment exécuter les scripts

#### Exécution de la pipeline complète (nettoyage + création du modèle)

Pour lancer l'ensemble du processus (nettoyage des données et création du modèle) depuis la racine du projet, utilisez le script `main.py` :

```bash
python main.py
```

Ce script va exécuter successivement :

1. **`clean.py` :** Nettoyage des données.
2. **`Model.py` :** Création et archivage du modèle.

#### Démarrage de MLflow

Avant d'exécuter `Model.py`, assurez-vous que MLflow est bien démarré. Pour ce faire, suivez ces étapes :

1. Placez-vous dans le dossier du projet :
   ```bash
   cd .\projet\
   cd .\model\
   ```

2. Lancez l'interface utilisateur de MLflow :
   ```bash
   mlflow ui
   ```

3. Accédez à l'interface MLflow à l'adresse suivante :
   ```plaintext
   http://127.0.0.1:5000
   ```

#### Exécution des tests

Il est important de tester la qualité des scripts avant de les utiliser en production. Les tests sont disponibles dans le dossier `tests` et peuvent être exécutés avec `pytest`.

1. Placez-vous dans le dossier des tests de l'API :
   ```bash
   cd .\projet\model\tests\
   ```

2. Exécutez les tests :
   ```bash
   pytest test_quality.py
   ```

Ces tests vérifieront :

- La connexion à la base de données.
- La suppression correcte des lignes avec un prix spécifique.
- La performance du modèle (R2 score) et l'absence de surajustement (overfitting).
- La validité des prédictions du modèle.

### Sauvegarde du Modèle

Le modèle entraîné est sauvegardé à deux endroits :

1. **MLflow :** Le modèle et ses métriques de performance sont enregistrés dans MLflow pour un suivi des versions.
2. **Pickle :** Le modèle est également sauvegardé sous forme de fichier pickle (`model.pkl`) pour une utilisation ultérieure.

Ces fichiers peuvent être utilisés pour charger et déployer le modèle via l'API dans les étapes suivantes.

### Commandes utiles

- **Lancer MLflow :**
  ```bash
  cd .\projet\
  cd .\model\
  mlflow ui
  ```

- **Exécuter les tests avec pytest :**
  ```bash
  cd .\projet\model\tests\
  pytest test_quality.py
  ```

Ce guide vous permet de configurer, exécuter, et tester la première étape du projet avec succès.   
N'oubliez pas de vérifier que toutes les dépendances sont correctement installées à partir de `requirements.txt` avant de lancer les scripts.




## Étape 2 : Lancement du MLOps avec Détection de Drift

Dans cette étape, nous allons explorer et monitorer notre modèle de machine learning en utilisant MLflow pour le suivi des métriques et Streamlit pour la visualisation interactive. Le dossier `ml_ops` contient deux fichiers principaux : un notebook `sand_box.ipynb` pour tester les fonctionnalités et un tableau de bord interactif `dashboard.py` déployé via Streamlit.

### Prérequis

Avant de commencer, assurez-vous que l'environnement de développement est correctement configuré et que toutes les dépendances sont installées. Veillez également à ce que le serveur MLflow soit opérationnel pour le suivi des expérimentations.

### 1. Lancer le Serveur MLflow

Tout d'abord, démarrez le serveur MLflow pour que vous puissiez suivre les performances du modèle.

```bash
cd .\projet\
cd .\model\
mlflow ui
```

Le serveur MLflow sera accessible à l'adresse suivante : [http://127.0.0.1:5000](http://127.0.0.1:5000).

### 2. Tester les Fonctionnalités avec `sand_box.ipynb`

Le fichier `sand_box.ipynb` est un notebook Jupyter où vous pouvez expérimenter avec les données, tester les modèles et visualiser les résultats. Ce notebook vous permet de :

- Charger et préparer les données depuis la base de données.
- Charger le modèle le plus récent archivé via MLflow.
- Visualiser les métriques de performance (R², MSE, MAE) directement depuis MLflow.
- Effectuer une détection de drift sur les caractéristiques sélectionnées.
- Comparer les prédictions du modèle sur les ensembles d'entraînement et de test.
- Analyser l'importance des caractéristiques du modèle.

### 3. Déployer le Tableau de Bord Interactif avec Streamlit

Pour une visualisation et une interaction en temps réel avec les résultats du modèle, lancez le tableau de bord Streamlit :

```bash
cd .\projet\
cd .\ml_ops\
streamlit run dashboard.py
```

Le tableau de bord sera disponible à l'adresse suivante : [http://localhost:8501](http://localhost:8501).

### 4. Utilisation du Tableau de Bord

Le tableau de bord Streamlit vous permet de :

- Visualiser les scores de performance du modèle actuel (R², MSE, MAE) directement dans l'interface.
- Sélectionner des caractéristiques pour effectuer une détection de drift. La distribution des données d'entraînement et de test pour la caractéristique sélectionnée sera affichée, et un test de Kolmogorov-Smirnov sera effectué pour détecter un drift potentiel.
- Comparer visuellement les prédictions du modèle avec les valeurs réelles pour les ensembles d'entraînement et de test.
- Visualiser l'importance des caractéristiques du modèle, avec un focus sur les 10 caractéristiques les plus influentes.

### Remarques

- **Détection de Drift** : Un avertissement s'affichera si un drift potentiel est détecté pour une caractéristique (p-value < 0.07).
- **Mises à Jour** : Si vous souhaitez tester de nouveaux modèles ou nouvelles versions, assurez-vous que MLflow est bien en marche et que le modèle est bien enregistré.

Cette étape vous permet d'exploiter au mieux les capacités de MLflow et de Streamlit pour un suivi continu et une analyse approfondie de vos modèles de machine learning.

---

Une fois l'étape 2 terminée, vous aurez un système complet de MLOps en place, permettant non seulement la création et l'archivage de modèles, mais aussi le suivi et la visualisation continue des performances des modèles avec une détection de drift intégrée.






## Étape 3 : Déploiement de l'API avec FastAPI pour les Prédictions

Dans cette étape, nous allons déployer une API en utilisant FastAPI qui servira à effectuer des prédictions à partir du modèle formé à l'étape 1. L'API sera conteneurisée à l'aide de Docker, et nous allons également écrire des tests pour valider son bon fonctionnement.

### 3.1 Préparation de l'Environnement

1. **Récupération du Modèle** : 
   Le modèle entraîné à l'étape 1 doit être récupéré sous forme de fichier `.pkl` (Pickle) et placé dans le dossier `api`. Ce modèle sera utilisé par l'API pour effectuer des prédictions.

2. **Variables d'Environnement** : 
   Assurez-vous que les variables d'environnement nécessaires sont définies dans un fichier `.env` situé dans le dossier `api`. Ce fichier doit contenir les informations de connexion à la base de données, ainsi que la clé secrète pour l'authentification via JWT.

### 3.2 Structure des Fichiers

Le dossier `api` contient les fichiers suivants :

- **main.py** : Le point d'entrée de l'application FastAPI.
- **predict.py** : Le fichier contenant la logique pour charger le modèle et effectuer des prédictions.
- **utils.py** : Contient des fonctions utilitaires, y compris l'authentification.
- **Dockerfile** : Le fichier Docker pour conteneuriser l'application.
- **tests/test_quality_api.py** : Les tests automatisés pour vérifier la qualité de l'API.

### 3.3 Déploiement avec FastAPI

Pour lancer l'API localement, suivez les étapes suivantes :

1. **Activer l'Environnement Virtuel** :

   ```bash
   cd ./projet/
   .\env\Scripts\activate
   cd ./api/
   ```

2. **Lancer l'API** :

   Exécutez la commande suivante pour démarrer le serveur FastAPI :

   ```bash
   uvicorn main:app --reload
   ```

   L'API sera disponible à l'adresse suivante : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Vous pouvez y tester les différentes routes de l'API.

### 3.4 Conteneurisation avec Docker

Pour conteneuriser l'application, suivez ces étapes :

1. **Construction de l'Image Docker** :

   Assurez-vous que vous êtes dans le répertoire `api` et exécutez la commande suivante :

   ```bash
   docker build -t api-prediction .
   ```

2. **Lancement du Conteneur** :

   Lancez le conteneur avec la commande suivante :

   ```bash
   docker run -d -p 8000:80 --env-file .env api-prediction
   ```

   L'API sera maintenant accessible via [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 3.5 Tests de Qualité

Le dossier `tests` contient des tests pour vérifier la qualité de l'API. Pour exécuter les tests, assurez-vous que l'API est en cours d'exécution, puis exécutez :

```bash
pytest tests/test_quality_api.py
```

Les tests couvrent les scénarios suivants :

- **Connexion à la Base de Données** : Vérifie si l'API peut se connecter à la base de données SQL Server.
- **Prédiction sans Authentification** : Vérifie que les prédictions sont refusées si l'utilisateur n'est pas authentifié.
- **Prédiction avec Authentification** : Vérifie que les prédictions sont possibles lorsque l'utilisateur est correctement authentifié.





## Étape 4 : Configuration CI/CD avec GitHub Actions

Dans cette étape, nous allons mettre en place un pipeline d'intégration continue (CI) et de déploiement continu (CD) en utilisant GitHub Actions. Ces pipelines automatiseront les tests et le déploiement de l'API à chaque `push` sur la branche `dev`. Les secrets nécessaires au pipeline sont stockés dans GitHub Secrets.

### 4.1 Fichiers de Configuration

Le dossier `.github/workflows/` contient deux fichiers YAML qui définissent les workflows CI et CD :

- **CI.yaml** : Ce workflow gère l'intégration continue, incluant l'installation des dépendances et l'exécution des tests.
- **CD.yaml** : Ce workflow gère le déploiement continu, incluant la construction et la publication de l'image Docker.

### 4.2 Détails du Workflow CI

Le fichier `CI.yaml` est configuré pour s'exécuter à chaque `push` sur la branche `dev`. Voici les étapes principales :

1. **Vérification du Code** :
   - Utilise l'action `checkout` pour récupérer le code source.
  
2. **Configuration de Python** :
   - Installe Python 3.10.8 pour correspondre à l'environnement de développement.

3. **Installation des Dépendances** :
   - Installe les dépendances nécessaires via `pip` en utilisant le fichier `projet/requirements.txt`.

4. **Exécution des Tests** :
   - Exécute les tests avec `pytest` pour s'assurer que le code est fonctionnel.


### 4.3 Détails du Workflow CD

Le fichier `CD.yaml` est également configuré pour s'exécuter à chaque `push` sur la branche `dev`. Ce workflow se charge de construire et de déployer l'image Docker de l'API. Voici les étapes principales :

1. **Installation de Docker** :
   - Met à jour le système et installe Docker sur une machine virtuelle Ubuntu.

2. **Connexion à Docker Hub** :
   - Se connecte à Docker Hub en utilisant les identifiants stockés dans GitHub Secrets.

3. **Construction et Publication de l'Image Docker** :
   - Construit l'image Docker en utilisant les secrets de la base de données et les autres variables d'environnement.
   - Pousse l'image Docker sur Docker Hub.


### 4.4 Exécution du Pipeline CI/CD

1. **Déposer les Secrets** : 
   - Déposez les informations sensibles telles que les identifiants Docker Hub et les informations de la base de données dans les secrets de votre dépôt GitHub (`Settings > Secrets and variables > Actions`).

2. **Pousser le Code sur la Branche `dev`** :
   - Chaque fois que vous poussez du code sur la branche `dev`, les workflows CI et CD s'exécuteront automatiquement.

3. **Vérification des Résultats** :
   - Vous pouvez suivre les logs et les résultats des workflows CI/CD dans l'onglet "Actions" de votre dépôt GitHub.

---

Cette section complète la mise en place d'un pipeline CI/CD robuste pour votre projet. Vous avez maintenant une automatisation complète des tests et du déploiement de votre API.