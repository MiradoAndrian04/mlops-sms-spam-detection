# Guide d'installation

## Ce dont tu as besoin

- Docker Desktop (installé et ouvert)
- Git (installé)
- Un navigateur web

---

## Étapes pour lancer le projet

### Étape 1 : Ouvrir un terminal

1. Appuie sur `Windows + X`
2. Clique sur **"Windows PowerShell"** ou **"Terminal"**

### Étape 2 : Aller dans le dossier du projet

```bash
cd C:\Users\mirad\Desktop\Etudes\M1\Docker\ProjetCICD
### Étape 3 : Aller dans le dossier docker
cd docker

### Étape 4 : Lancer les conteneurs
bash
docker compose up -d

Vous devriez voir :
text
[+] Running 3/3
 ✔ Container spam_mlflow      Started
 ✔ Container spam_api         Started
 ✔ Container spam_streamlit   Started

### Étape 5 : Vérifier que tout tourne
docker ps

Vous devriez voir 3 conteneurs :
- spam_api
- spam_streamlit
- spam_mlflow

### Étape 6 : Tester l'application

Ouvrez votre navigateur et testez ces adresses :
Interface Streamlit	: http://localhost:8501
API FastAPI :	http://localhost:8000/docs
MLflow UI : http://localhost:5000

## Étapes pour arrêter les services
### Étape 1 : Aller dans le dossier docker
cd C:\Users\mirad\Desktop\Etudes\M1\Docker\ProjetCICD\docker
### Étape 2 : Arrêter tout

docker compose down