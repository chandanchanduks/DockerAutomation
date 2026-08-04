pipeline {
    agent any
    parameters{
        booleanParam(name:"BUILD_IMAGE",defaultValue:true,description:"build images if selected")
        booleanParam(name:"CLEAN_UP",defaultValue:true,description:"will stop the compose at end by default")
        choice(name:"ENVIRONMENT",choices:["PROD","DEV","QA"],description:"select the environment to run")
    }

    environment {
        PROJECT_NAME = "DockerAutomation"
        CONTAINER_NAME="automation"
        CONTAINER_REPORT_FOLDER="/automation/reports"
    }

    stages {
        stage("Running Environment"){
            steps{
                script {
                    switch (params.ENVIRONMENT) {
                        case "PROD":
                            echo "Running on Production"
                            break

                        case "QA":
                            echo "Running on QA"
                            break

                        case "DEV":
                            echo "Running on Development"
                            break

                        default:
                            error "Unknown Environment"
                    }
                }
            }
        }
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
                script{
                    if(params.BUILD_IMAGE){
                    sh '''
                    docker compose down || true
                    docker compose up --build -d
                    '''
                }else{
                sh "docker compose up -d"
                }
                // sh '''
                //     docker compose down || true
                //     docker compose up --build -d
                // '''
            }
        }
        stage('Wait For Automation') {
            steps {
                script {
                    env.AUTOMATION_CID = sh(
                        script: "docker compose ps -aq ${CONTAINER_NAME}",
                        returnStdout: true
                    ).trim()
                }

                sh '''
                    docker wait "$AUTOMATION_CID"
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
                    mkdir -p automation_reports

                    docker cp "$AUTOMATION_CID":${CONTAINER_REPORT_FOLDER}/. automation_reports/

                    ls -R automation_reports
                '''
            }
        }
        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'automation_reports/**', fingerprint: true
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
            script{
                if(params.CLEAN_UP){
                sh "docker compose down || true"
            }else{
                echo "Skipping build cleanup"
            }
            }
        }
    }
}