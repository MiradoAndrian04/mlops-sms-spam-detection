import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MODEL_PATH = os.path.join(BASE_DIR, "mlruns", "spam_detector_model.pkl")

if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.join(BASE_DIR, "src", "model", "spam_detector_model.pkl")

API_HOST = "0.0.0.0"
API_PORT = 8000
API_RELOAD = True

CORS_ORIGINS = ["*"] 