# Utiliser une image de base avec Python
FROM python:3.9-slim

# Copier les fichiers de l'application dans le conteneur
COPY . /app_exercice

# Définir le répertoire de travail dans le conteneur
WORKDIR /app_exercice

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application Flask s'exécute
EXPOSE 5000

# Commande pour démarrer l'application Flask
CMD ["python", "app.py"]
