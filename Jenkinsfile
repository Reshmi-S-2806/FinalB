pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling Project code from GitHub...'
                git branch: 'main', url: 'https://github.com/Reshmi-S-2806/ProjectBackend.git'
            }
        }

        stage('Docker Build - All Services') {
            steps {
                echo 'Building 1/3: Main Node.js Backend...'
                bat 'docker build -t shopeasy-backend:latest .'

                echo 'Building 2/3: Python Fraud Detection Service...'
                // We move into the specific folder to run the build
                dir('fraud-service') {
                    bat 'docker build -t shopeasy-fraud:v1 .'
                }

                echo 'Building 3/3: Python Chatbot Service...'
                dir('chatbot-service') {
                    bat 'docker build -t shopeasy-chatbot:v1 .'
                }
            }
        }

        stage('Kubernetes Deploy') {
            steps {
                echo 'Applying Kubernetes Configurations...'
                // This applies all deployments and services in your k8s folder
                bat 'kubectl apply -f k8s/deployment.yaml'
                bat 'kubectl apply -f k8s/service.yaml'
                
                echo 'Restarting Deployments to pull the new local images...'
                bat 'kubectl rollout restart deployment/shopeasy-backend'
                bat 'kubectl rollout restart deployment/shopeasy-fraud'
                bat 'kubectl rollout restart deployment/shopeasy-chatbot'
                
                echo 'All services are now live!'
            }
        }
    }
}
