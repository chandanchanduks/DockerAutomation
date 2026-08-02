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
                    docker wait $(docker compose ps -q automation)
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

                mkdir -p automation_reports

                docker cp $(docker compose ps -q automation):/automation/reports/. automation_reports/

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