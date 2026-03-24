pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling Backend code...'
                git branch: 'main', url: 'https://github.com/Reshmi-S-2806/ProjectBackend.git'
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Backend Image (Installing Node & Python inside)...'
                // This command triggers the 'npm install' and 'pip install' inside the Dockerfile
                bat 'docker build -t shopeasy-backend:latest .'
            }
        }

        stage('Kubernetes Deploy') {
            steps {
                echo 'Deploying Backend to K8s...'
                bat 'kubectl apply -f k8s/deployment.yaml'
                bat 'kubectl apply -f k8s/service.yaml'
                bat 'kubectl rollout restart deployment/shopeasy-backend'
                echo 'Backend is now live and connecting to postgres-service:5432'
            }
        }
    }
}
