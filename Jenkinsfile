pipeline{
    agent any
    stages{
        stage("cloning from Github..."){
            steps{
                script{
                    echo 'cloning from github...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops_project', url: 'https://github.com/Yeshwanththota/mlops_project2.git']])
                }
            }
        }
    }
}