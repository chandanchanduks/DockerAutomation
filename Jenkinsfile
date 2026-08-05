pipeline {
    agent any

    parameters {
        booleanParam(
            name: 'BUILD_IMAGE',
            defaultValue: true,
            description: 'Build Docker images before starting'
        )

        booleanParam(
            name: 'CLEAN_UP',
            defaultValue: true,
            description: 'Stop and remove containers after pipeline'
        )

        choice(
            name: 'ENVIRONMENT',
            choices: ['DEV', 'QA', 'PROD'],
            description: 'Select execution environment'
        )
        choice(
        name: 'TEST_SUITE',
        choices: ['Smoke','Regression','Sanity'],
        description: 'Select Test Suite'
    )

    }

    environment {
        PROJECT_NAME = "DockerAutomation"
        CONTAINER_NAME = "automation"
        CONTAINER_REPORT_FOLDER = "/automation/reports"
    }

    stages {

        stage('Running Environment') {
            steps {
                script {
                    switch(params.ENVIRONMENT) {

                        case "DEV":
                            echo "Running on Development Environment"
                            break

                        case "QA":
                            echo "Running on QA Environment"
                            break

                        case "PROD":
                            echo "Running on Production Environment"
                            break

                        default:
                            error "Invalid Environment Selected"
                    }
                }
            }
        }

        stage('Workspace') {
            steps {
                sh '''
                    echo "===== Current Directory ====="
                    pwd

                    echo "===== Workspace Files ====="
                    ls -la
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                script {

                    if (params.BUILD_IMAGE) {

                        sh """
                            docker compose down || true
                            TEST_SUITE=${params.TEST_SUITE} docker compose up --build -d
                        """

                    } else {

                        sh """
                            TEST_SUITE=${params.TEST_SUITE} docker compose up -d
                        """

                    }

                }
            }
        }

        stage('Wait For Automation Container') {
            steps {

                script {

                    env.AUTOMATION_CID = sh(
                        script: "docker compose ps -aq ${CONTAINER_NAME}",
                        returnStdout: true
                    ).trim()

                    echo "Automation Container ID : ${env.AUTOMATION_CID}"

                    sh "docker wait ${env.AUTOMATION_CID}"

                }

            }
        }

        stage('Container Logs') {
            steps {

                sh '''
                    echo "===== Container Logs ====="
                    docker compose logs
                '''

            }
        }

        stage('Collect Reports') {
            steps {

                sh '''
                    mkdir -p automation_reports

                    docker cp "$AUTOMATION_CID":"$CONTAINER_REPORT_FOLDER"/. automation_reports/

                    echo "===== Reports ====="

                    ls -R automation_reports
                '''

            }
        }

        stage('Archive Reports') {
            steps {

                archiveArtifacts(
                    artifacts: 'automation_reports/**',
                    fingerprint: true
                )

            }
        }

    }

    post {

        success {
            echo "Pipeline Completed Successfully"
        }

        failure {
            echo "Pipeline Failed"
        }

        always {

            script {

                if (params.CLEAN_UP) {

                    sh '''
                        docker compose down || true
                    '''

                } else {

                    echo "Cleanup Skipped"

                }

            }

        }

    }
}