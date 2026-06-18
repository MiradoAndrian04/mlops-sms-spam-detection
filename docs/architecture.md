# Architecture du projet

## Les 4 composants principaux

### 1. Interface Streamlit (port 8501)
- C'est l'écran que l'utilisateur voit
- Il contient un champ pour saisir un SMS et un bouton "Analyser"
- Il envoie le SMS à l'API et affiche le résultat

### 2. API FastAPI (port 8000)
- C'est le cerveau de l'application
- Elle reçoit le SMS, le nettoie, fait la prédiction et renvoie le résultat
- Elle est documentée automatiquement sur http://localhost:8000/docs

### 3. MLflow (port 5000)
- C'est le gestionnaire de modèles
- Il garde un historique de tous les modèles entraînés
- Il stocke les métriques (précision, F1-score, etc.)

### 4. SQLite (base de données)
- C'est le stockage des données MLflow
- Fichier : `mlflow.db`

## Comment les composants communiquent
L'utilisateur saisit un SMS dans Streamlit

Streamlit envoie le SMS à l'API FastAPI

L'API utilise le modèle MLflow pour prédire

Le résultat (spam/ham) est renvoyé à Streamlit

Streamlit affiche le résultat à l'utilisateur

## Le pipeline CI/CD (automatisation)
Le développeur pousse du code sur GitHub

Jenkins détecte le changement

Jenkins construit les images Docker

Jenkins pousse les images sur Docker Hub

Jenkins déploie l'application


## Schéma simple
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Streamlit │────▶│ FastAPI │────▶│ Modèle │
│ (8501) │ │ (8000) │ │ MLflow │
└─────────────┘ └─────────────┘ └─────────────┘
│ │ │
└────────────────────┼────────────────────┘
▼
┌─────────────┐
│ SQLite │
│ (mlflow.db)│
└─────────────┘

