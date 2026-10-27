
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'college-notice-board:1.0'
        DEPLOYMENT_NAME = 'college-notice-board'
        CONTAINER_NAME = 'college-notice-board'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building the Docker image'
                bat 'docker build -t college-notice-board:1.0 .'
            }
        }

        stage('Verify Kubernetes') {
            steps {
                echo 'Checking Kubernetes cluster'
                bat 'kubectl get nodes'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Applying Kubernetes configuration'
                bat 'kubectl apply -f k8s-deployment.yaml'
                bat 'kubectl rollout status deployment/college-notice-board --timeout=120s'
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'kubectl get pods'
                bat 'kubectl get services'
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully!'
            echo 'Website: http://localhost:30090'
        }

        failure {
            echo 'Pipeline failed. Check the Jenkins console output.'
        }
    }
}
