import os

# Chemins des dossiers
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Chemin du modèle
MODEL_PATH = os.path.join(BASE_DIR, "mlruns", "spam_detector_model.pkl")

# Si le modèle n'existe pas à cet emplacement
if not os.path.exists(MODEL_PATH):
    # Essayer dans src/model
    MODEL_PATH = os.path.join(BASE_DIR, "src", "model", "spam_detector_model.pkl")

# Configuration de l'API
API_HOST = "0.0.0.0"
API_PORT = 8000
API_RELOAD = True  # False en production

# Configuration CORS
CORS_ORIGINS = ["*"]  # En production, mettre les domaines autorisés