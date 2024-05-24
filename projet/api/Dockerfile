# Utiliser une image de base Python 3.10.8
FROM python:3.10.8

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances nécessaires pour pyodbc et le pilote ODBC pour SQL Server
RUN apt-get update && apt-get install -y g++ unixodbc-dev curl curl ca-certificates
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code dans le répertoire de travail
COPY . .

# Ajouter les variables d'environnement à partir du fichier .env
ARG DB_SERVER
ARG DB_DATABASE
ARG DB_USERNAME
ARG DB_PASSWORD
ARG SECRET_KEY
ARG TOKEN

ENV DB_SERVER=$DB_SERVER
ENV DB_DATABASE=$DB_DATABASE
ENV DB_USERNAME=$DB_USERNAME
ENV DB_PASSWORD=$DB_PASSWORD
ENV SECRET_KEY=$SECRET_KEY
ENV TOKEN=$TOKEN

# Exposer le port sur lequel l'application s'exécute
EXPOSE 8000

# Définir la commande pour exécuter l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
