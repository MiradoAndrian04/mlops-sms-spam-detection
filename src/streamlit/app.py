import streamlit as st
import requests
import time
import json
from typing import Dict, Any
import os

import streamlit as st
import requests
import os


API_URL = os.getenv("API_URL", "http://localhost:8000/predict")

st.set_page_config(page_title="SMS Spam Detector", layout="centered")

# DEBUG - Afficher l'URL utilisée
st.title(" Détection de SMS Spam")

message = st.text_area("Saisissez votre SMS", height=120)

if st.button(" Analyser"):
    if not message.strip():
        st.warning("Veuillez saisir un SMS")
    else:
        try:
            response = requests.post(API_URL, json={"message": message}, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("is_spam"):
                    st.error(f" SPAM - Confiance: {result.get('confidence', 0):.1%}")
                else:
                    st.success(f" HAM - Confiance: {result.get('confidence', 0):.1%}")
            else:
                st.error(f"Erreur API: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error(f" Impossible de se connecter à l'API sur {API_URL}")
        except Exception as e:
             st.error(f" Erreur: {str(e)}")

with st.expander(" Exemples de SMS à tester", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("Exemples de SPAM :")
        st.code("Congratulations! You've won a free iPhone. Click here to claim your prize!", language="text")
        st.code("URGENT! Your bank account has been compromised. Call now!", language="text")
        st.code("FREE entry to win a holiday worth £1000", language="text")
    
    with col2:
        st.markdown(" Exemples de HAM :")
        st.code("Hey, I'll be late for dinner. Traffic is terrible.", language="text")
        st.code("Don't forget our meeting at 3pm tomorrow.", language="text")
        st.code("I'll pick you up at the airport at 5pm.", language="text")

# Métadonnées
st.markdown("""
    <div class="metadata">
         Modèle : TF-IDF + Logistic Regression &nbsp;|&nbsp; 
         F1-Score : 0.97 &nbsp;|&nbsp; 
         API : FastAPI &nbsp;|&nbsp; 
         Interface : Streamlit
    </div>
""", unsafe_allow_html=True)