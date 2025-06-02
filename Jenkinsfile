pipeline{
    agent any
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "lofty-voyage-461011-f1"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
    }
    stages{
        stage("cloning from Github..."){
            steps{
                script{
                    echo 'cloning from github...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops_project', url: 'https://github.com/Yeshwanththota/mlops_project2.git']])
                }
            }

        }
        stage('Setting up our Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing dependancies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install dvc
                    '''
                }
            }
        }
        stage("DVC Pull"){
            steps{
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Pulling data from DVC...'
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
            }
        }
        stage("Building Docker Image"){
            steps{
                script{
                    withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                        script{
                            echo 'Building Docker Image...'
                            sh '''
                            export PATH=$PATH:$(GCLOUD_PATH)
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                            gcloud auth configure-docker --quiet
                            docker build -t gcr.io/${GCP_PROJECT}/mlops_project2:latest .
                            docker push gcr.io/${GCP_PROJECT}/mlops_project2:latest
                            '''
                        }
                    }
                }
            }
        }
        stage("Deploying to GKE"){
            steps{
                script{
                    withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                        script{
                            echo 'Deploying to GKE...'
                            sh '''
                            export PATH=$PATH:$(GCLOUD_PATH):{KUBECTL_AUTH_PLUGIN}
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                            gcloud container clusters get-credentials autopilot-cluster-1 --zone us-central1 --project ${GCP_PROJECT}
                            kubectl apply -f deployment.yaml
                            
                            '''
                        }
                    }
                }
            }
        }
    }
}