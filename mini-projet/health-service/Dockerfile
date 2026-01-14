# On utilise une version légère de Python
FROM python:3.9-slim

# Dossier de travail
WORKDIR /app

# On installe les dépendances directement (plus simple pour ce TP)
RUN pip install flask flask-sqlalchemy flask-cors requests pyjwt

# On copie tout le code
COPY . .

# La commande de lancement sera définie par le docker-compose
CMD ["python", "app.py"]