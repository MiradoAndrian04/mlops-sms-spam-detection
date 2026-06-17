import os
import sys
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any
import uvicorn
import re
import string

#Configuration

# Ajouter le chemin du projet pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Chemin du modèle (ajuste selon ta structure)
MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "mlruns",
    "spam_detector_model.pkl"
)

# Si le modèle n'est pas dans mlruns, essaie dans src/model
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "model",
        "spam_detector_model.pkl"
    )

print(f"📁 Chargement du modèle depuis : {MODEL_PATH}")

#Chargement du modèle

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Modèle chargé avec succès !")
except Exception as e:
    print(f"❌ Erreur lors du chargement du modèle : {e}")
    model = None

#Fonctions et pretraitement

def clean_text(text: str) -> str:
    """
    Nettoie le texte d'un SMS (identique au preprocessing d'entraînement)
    """
    # Convertir en minuscules
    text = text.lower()
    
    # Supprimer la ponctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Supprimer les chiffres
    text = re.sub(r'\d+', '', text)
    
    # Supprimer les espaces superflus
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

#Model Pydantic

class SMSRequest(BaseModel):
    """
    Modèle de requête pour la prédiction
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Le message SMS à analyser",
        example="Congratulations! You've won a free iPhone"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Congratulations! You've won a free iPhone"
            }
        }

class SMSResponse(BaseModel):
    """
    Modèle de réponse pour la prédiction
    """
    prediction: str = Field(..., description="Résultat de la prédiction : 'spam' ou 'ham'")
    confidence: float = Field(..., description="Niveau de confiance de la prédiction (0-1)")
    is_spam: bool = Field(..., description="True si spam, False si ham")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prediction": "spam",
                "confidence": 0.987,
                "is_spam": True
            }
        }

class HealthResponse(BaseModel):
    """
    Modèle de réponse pour le health check
    """
    status: str
    model_loaded: bool
    version: str

#Application FastAPI

app = FastAPI(
    title="SMS Spam Detection API",
    description="API de détection de SMS spam utilisant un modèle TF-IDF + Logistic Regression",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurer CORS (pour permettre à Streamlit de communiquer avec l'API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, restreindre aux domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Endpoints

@app.get("/", response_model=Dict[str, str])
async def root():
    """
    Endpoint racine
    """
    return {
        "message": "API de détection de SMS Spam",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Vérifie l'état de l'API et du modèle
    """
    return HealthResponse(
        status="healthy" if model is not None else "unhealthy",
        model_loaded=model is not None,
        version="1.0.0"
    )

@app.post("/predict", response_model=SMSResponse)
async def predict(request: SMSRequest):
    """
    Prédit si un SMS est un spam ou un ham
    
    - **message**: Le texte du SMS à analyser
    """
    # Vérifier que le modèle est chargé
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Le modèle n'est pas chargé. Veuillez réessayer plus tard."
        )
    
    try:
        # 1. Nettoyer le texte
        cleaned_message = clean_text(request.message)
        
        # 2. Faire la prédiction
        prediction = model.predict([cleaned_message])[0]
        probabilities = model.predict_proba([cleaned_message])[0]
        
        # 3. Interpréter les résultats
        is_spam = bool(prediction == 1)
        confidence = float(probabilities[1] if is_spam else probabilities[0])
        label = "spam" if is_spam else "ham"
        
        # 4. Retourner la réponse
        return SMSResponse(
            prediction=label,
            confidence=confidence,
            is_spam=is_spam
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la prédiction : {str(e)}"
        )

#Gestion des erreurs

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Gestionnaire d'erreurs HTTP
    """
    return {
        "error": True,
        "status_code": exc.status_code,
        "detail": exc.detail
    }

#Point d'entrée pour le lancement

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )