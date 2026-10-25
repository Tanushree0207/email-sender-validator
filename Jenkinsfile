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
    }

    post {
        success {
            echo 'Build successful! All automated tests passed.'
        }
        failure {
            echo 'Build failed. Check the console output for errors.'
        }
    }
}
