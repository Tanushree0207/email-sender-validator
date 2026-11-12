
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv .jenkins-venv
                    .jenkins-venv/bin/pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '.jenkins-venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Automated Tests') {
            steps {
                sh '.jenkins-venv/bin/python -m pytest -v'
            }
        }

        stage('Package Project') {
            steps {
                sh '''
                    tar --exclude='.git' \
                        --exclude='venv' \
                        --exclude='.jenkins-venv' \
                        --exclude='__pycache__' \
                        --exclude='.pytest_cache' \
                        -czf email-sender-validator.tar.gz .
                '''
            }
        }

        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'email-sender-validator.tar.gz', fingerprint: true
            }
        }
    }
}
