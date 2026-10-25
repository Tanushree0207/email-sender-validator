
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Automated Tests') {
            steps {
                sh './venv/bin/python -m pytest -v'
            }
        }

        stage('Package Artifact') {
            steps {
                sh 'tar -czf email-sender-validator.tar.gz app.py requirements.txt Jenkinsfile tests/'
                archiveArtifacts artifacts: 'email-sender-validator.tar.gz', fingerprint: true
            }
        }
    }

    post {
        success {
            echo 'Build successful! All automated tests passed and artifact archived.'
        }
        failure {
            echo 'Build failed. Check the console output for errors.'
        }
    }
}

