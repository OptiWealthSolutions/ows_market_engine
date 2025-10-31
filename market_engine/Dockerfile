# Utilise une image Python légère officielle
FROM python:3.11-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les dépendances et les installe en premier pour optimiser le cache Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code de l'application
COPY . .

# Expose le port par défaut de FastAPI (sera utilisé par l'API)
EXPOSE 8000

# Commande par défaut (sera surchargée dans docker-compose.yml)
CMD ["echo", "Ready to run"]