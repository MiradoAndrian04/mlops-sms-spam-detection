@echo off
echo ============================================
echo  LANCEMENT DES CONTENEURS
echo ============================================

cd /d "%~dp0"

echo  Construction des images...
docker compose build

echo  Lancement des conteneurs...
docker compose up -d

echo.
echo  Conteneurs lancés !
echo.
echo  Vérification :
docker ps

echo.
echo  Accès aux services :
echo     Streamlit : http://localhost:8501
echo     API       : http://localhost:8000/docs
echo     MLflow    : http://localhost:5000
echo.
echo Pour voir les logs : docker compose logs -f
echo Pour arrêter       : docker compose down

pause