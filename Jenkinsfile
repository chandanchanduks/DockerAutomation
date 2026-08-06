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
        TEST_SUITE = "${params.TEST_SUITE}"
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_USERNAME   = "chandankatterishashikumar"
        DOCKER_REPOSITORY = "dockerautomation-pipeline"
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
                            IMAGE_TAG=${IMAGE_TAG} docker compose up --build -d
                        """

                    } else {

                        sh """
                            IMAGE_TAG=${IMAGE_TAG} docker compose up -d
                        """

                    }

                }
            }
        }
        stage('Verify Images') {
            steps {
                sh '''
                    docker image inspect dockerautomation-pipeline-automation:${IMAGE_TAG}

                    docker image inspect dockerautomation-pipeline-device:${IMAGE_TAG}

                    echo "Images Verified Successfully"
                '''
            }
        }
        stage('Tag Latest') {
            steps {
                sh '''
                    docker tag \
                    dockerautomation-pipeline-automation:${IMAGE_TAG} \
                    dockerautomation-pipeline-automation:latest

                    docker tag \
                    dockerautomation-pipeline-device:${IMAGE_TAG} \
                    dockerautomation-pipeline-device:latest
                '''
            }
        }
        stage('Verify Tags') {
            steps {
                sh '''
                    docker image inspect dockerautomation-pipeline-automation:${IMAGE_TAG}

                    docker image inspect dockerautomation-pipeline-automation:latest

                    docker image inspect dockerautomation-pipeline-device:${IMAGE_TAG}

                    docker image inspect dockerautomation-pipeline-device:latest

                    echo "All tags verified."
                '''
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
        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login \
                        -u "$DOCKER_USER" \
                        --password-stdin
                    '''
                }
            }
        }
        stage('Retag Images') {
            steps {
                sh '''
                    echo "===== Retagging Images ====="

                    docker tag \
                    dockerautomation-pipeline-automation:${IMAGE_TAG} \
                    ${DOCKER_USERNAME}/${DOCKER_REPOSITORY}:${IMAGE_TAG}

                    docker tag \
                    dockerautomation-pipeline-automation:${IMAGE_TAG} \
                    ${DOCKER_USERNAME}/${DOCKER_REPOSITORY}:latest
                '''
            }
        }
        stage('Verify Retag') {
            steps {
                sh '''
                    echo "===== Verifying Tags ====="

                    docker image inspect \
                    ${DOCKER_USERNAME}/${DOCKER_REPOSITORY}:${IMAGE_TAG}

                    docker image inspect \
                    ${DOCKER_USERNAME}/${DOCKER_REPOSITORY}:latest

                    echo "Retag Successful"
                '''
            }
        }
        stage('Push Version Image') {
            steps {
                sh '''
                    echo "===== Pushing Version Image ====="

                    ${DOCKER_USERNAME}/${DOCKER_REPOSITORY}:${IMAGE_TAG}
                '''
            }
        }
        stage('Push Latest Image') {
            steps {
                sh '''
                    echo "===== Pushing Latest Image ====="

                    ${DOCKER_USERNAME}/${DOCKER_REPOSITORY}:latest
                '''
            }
        }
        stage('Verify Push') {
            steps {
                sh '''
                    echo "===== Verifying Docker Hub Image ====="

                    docker pull ${DOCKER_USERNAME}/${DOCKER_REPOSITORY}:${IMAGE_TAG}

                    echo "Image Successfully Pulled"
                '''
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