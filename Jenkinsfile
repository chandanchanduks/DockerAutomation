pipeline {

    agent any

    parameters {

        booleanParam(
            name: 'BUILD_IMAGE',
            defaultValue: true,
            description: 'Build Docker Images'
        )

        booleanParam(
            name: 'CLEAN_UP',
            defaultValue: true,
            description: 'Cleanup Containers'
        )

        choice(
            name: 'ENVIRONMENT',
            choices: ['DEV', 'QA', 'PROD'],
            description: 'Execution Environment'
        )

        choice(
            name: 'TEST_SUITE',
            choices: ['Smoke', 'Regression', 'Sanity'],
            description: 'Select Test Suite'
        )

    }

    environment {

        PROJECT_NAME = "DockerAutomation"

        IMAGE_TAG = "${BUILD_NUMBER}"

        CONTAINER_NAME = "automation"

        REPORT_FOLDER = "/automation/reports"

        DEVICE_IMAGE = "dockerautomation-pipeline-device"

        AUTOMATION_IMAGE = "dockerautomation-pipeline-automation"

        DOCKER_USERNAME = "chandankatterishashikumar"

    }

    stages {

        stage('Execution Environment') {

            steps {

                script {

                    switch(params.ENVIRONMENT) {

                        case "DEV":
                            echo "Running on DEV"
                            break

                        case "QA":
                            echo "Running on QA"
                            break

                        case "PROD":
                            echo "Running on PROD"
                            break

                        default:
                            error "Invalid Environment"

                    }

                    echo "Test Suite : ${params.TEST_SUITE}"

                }

            }

        }

        stage('Workspace') {

            steps {

                sh '''

                echo "===== Current Directory ====="

                pwd

                echo

                echo "===== Workspace Files ====="

                ls -la

                '''

            }

        }

        stage('Checkout') {

            steps {

                checkout scm

            }

        }

        stage('Build Docker Images') {

            steps {

                script {

                    if(params.BUILD_IMAGE){

                        sh """

                        docker compose down || true

                        IMAGE_TAG=${IMAGE_TAG} \
                        TEST_SUITE=${params.TEST_SUITE} \
                        docker compose up --build -d

                        """

                    }

                    else{

                        sh """

                        IMAGE_TAG=${IMAGE_TAG} \
                        TEST_SUITE=${params.TEST_SUITE} \
                        docker compose up -d

                        """

                    }

                }

            }

        }

        stage('Verify Images') {

            steps {

                sh """

                docker image inspect ${DEVICE_IMAGE}:${IMAGE_TAG}

                docker image inspect ${AUTOMATION_IMAGE}:${IMAGE_TAG}

                echo

                echo "Images Verified Successfully"

                """

            }

        }

        stage('Wait For Automation Container') {

            steps {

                script {

                    env.AUTOMATION_CID = sh(

                        script: "docker compose ps -aq ${CONTAINER_NAME}",

                        returnStdout: true

                    ).trim()

                    echo "Automation Container : ${env.AUTOMATION_CID}"

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

                sh """

                mkdir -p automation_reports

                docker cp ${AUTOMATION_CID}:${REPORT_FOLDER}/. automation_reports/

                echo

                echo "===== Reports Collected ====="

                ls -R automation_reports

                """

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

                    echo "===== Docker Login ====="

                    echo "$DOCKER_PASS" | docker login \
                    -u "$DOCKER_USER" \
                    --password-stdin

                    '''

                }

            }

        }

        stage('Retag Images') {

            steps {

                sh """

                echo "===== Retagging Device Image ====="

                docker tag \
                ${DEVICE_IMAGE}:${IMAGE_TAG} \
                ${DOCKER_USERNAME}/${DEVICE_IMAGE}:${IMAGE_TAG}

                docker tag \
                ${DEVICE_IMAGE}:${IMAGE_TAG} \
                ${DOCKER_USERNAME}/${DEVICE_IMAGE}:latest


                echo "===== Retagging Automation Image ====="

                docker tag \
                ${AUTOMATION_IMAGE}:${IMAGE_TAG} \
                ${DOCKER_USERNAME}/${AUTOMATION_IMAGE}:${IMAGE_TAG}

                docker tag \
                ${AUTOMATION_IMAGE}:${IMAGE_TAG} \
                ${DOCKER_USERNAME}/${AUTOMATION_IMAGE}:latest

                """

            }

        }

        stage('Verify Retag') {

            steps {

                sh """

                echo "===== Verifying Local Tags ====="

                docker image inspect \
                ${DOCKER_USERNAME}/${DEVICE_IMAGE}:${IMAGE_TAG}

                docker image inspect \
                ${DOCKER_USERNAME}/${DEVICE_IMAGE}:latest

                docker image inspect \
                ${DOCKER_USERNAME}/${AUTOMATION_IMAGE}:${IMAGE_TAG}

                docker image inspect \
                ${DOCKER_USERNAME}/${AUTOMATION_IMAGE}:latest

                """

            }

        }

        stage('Push Version Images') {

            steps {

                sh """

                echo "===== Pushing Version Images ====="

                docker push \
                ${DOCKER_USERNAME}/${DEVICE_IMAGE}:${IMAGE_TAG}

                docker push \
                ${DOCKER_USERNAME}/${AUTOMATION_IMAGE}:${IMAGE_TAG}

                """

            }

        }

        stage('Push Latest Images') {

            steps {

                sh """

                echo "===== Pushing Latest Images ====="

                docker push \
                ${DOCKER_USERNAME}/${DEVICE_IMAGE}:latest

                docker push \
                ${DOCKER_USERNAME}/${AUTOMATION_IMAGE}:latest

                """

            }

        }

        stage('Verify Docker Hub Images') {

            steps {

                sh """

                echo "===== Pulling Images From Docker Hub ====="

                docker pull \
                ${DOCKER_USERNAME}/${DEVICE_IMAGE}:${IMAGE_TAG}

                docker pull \
                ${DOCKER_USERNAME}/${AUTOMATION_IMAGE}:${IMAGE_TAG}

                echo

                echo "Docker Hub Verification Successful"

                """

            }

        }

    }

    post {

        success {

            echo "====================================="
            echo "Pipeline Completed Successfully"
            echo "====================================="

        }

        failure {

            echo "====================================="
            echo "Pipeline Failed"
            echo "====================================="

        }

        always {

            script {

                if(params.CLEAN_UP){

                    sh '''

                    echo "===== Cleaning Containers ====="

                    docker compose down || true

                    '''

                }

                else{

                    echo "Cleanup Skipped"

                }

            }

        }

    }

}