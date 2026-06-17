pipeline {
    agent any

    environment {
        DOCKER_IMAGE_API = 'miradoandrian04/mlops-spam-api'
        DOCKER_IMAGE_STREAMLIT = 'miradoandrian04/mlops-spam-streamlit'
        DOCKER_IMAGE_MLFLOW = 'miradoandrian04/mlops-spam-mlflow'
    }

    stages {
        stage('Checkout') {
            steps {
                echo ' Récupération du code depuis GitHub...'
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                echo ' Construction des images Docker...'
                script {
                    sh """
                        echo ' Construction de l'API...'
                        docker build -f docker/Dockerfile.api -t ${DOCKER_IMAGE_API}:latest .
                        
                        echo ' Construction de Streamlit...'
                        docker build -f docker/Dockerfile.streamlit -t ${DOCKER_IMAGE_STREAMLIT}:latest .
                        
                        echo ' Construction de MLflow...'
                        docker build -f docker/Dockerfile.mlflow -t ${DOCKER_IMAGE_MLFLOW}:latest .
                    """
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo ' Push des images vers Docker Hub...'
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )]) {
                        sh """
                            echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USER} --password-stdin
                            docker push ${DOCKER_IMAGE_API}:latest
                            docker push ${DOCKER_IMAGE_STREAMLIT}:latest
                            docker push ${DOCKER_IMAGE_MLFLOW}:latest
                        """
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                echo ' Déploiement terminé !'
            }
        }
    }

    post {
        success {
            echo ' Pipeline réussi !'
        }
        failure {
            echo ' Pipeline échoué. Vérifie les logs.'
        }
    }
}