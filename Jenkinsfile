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
                    CID=$(docker compose ps -aq automation)
                    docker wait "$CID"
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
        stage('Collect Reports') {
            steps {
                sh '''
                echo "========== Copy Reports =========="

                CID=$(docker compose ps -aq automation)
                mkdir -p automation_reports
                docker cp "$CID":/automation/reports/. automation_reports/

                echo "========== Reports =========="
                ls -R automation_reports
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