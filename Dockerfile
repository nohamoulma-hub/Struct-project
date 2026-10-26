# Image de base : Python 3.12, plus récent que les 3.10 demandés par le SDK
FROM python:3.12-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# Installe le SDK Claude Agent SDK à l'intérieur du conteneur, pas sur le Mac
RUN pip install --no-cache-dir claude-agent-sdk

# Copie le repo dans le conteneur (sauf ce que .dockerignore exclut)
COPY . .

# Lance le test sur le premier projet type
CMD ["python3", "scripts/lancer_projet_type.py", "projets-types/prise-de-rendez-vous.md"]
