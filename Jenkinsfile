pipeline {
    agent any

    environment {
        PROJECT_NAME = "DockerAutomation"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "===== Workspace ====="
                sh 'pwd'

                echo "===== Files ====="
                sh 'ls -la'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    docker compose down || true
                    docker compose up --build -d
                '''
            }
        }

        stage('Wait For Automation') {
            steps {
                sh '''
                    docker wait automation_v1
                '''
            }
        }

        stage('Container Logs') {
            steps {
                sh '''
                    docker compose logs
                '''
            }
        }

    }

    post {

        success {
            echo "Pipeline SUCCESS"
        }

        failure {
            echo "Pipeline FAILED"
        }

        always {
            sh 'docker compose down || true'
        }
    }
}