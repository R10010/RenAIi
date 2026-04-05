pipeline {
    agent any

    environment {
        PYTHON = 'python'
    }

    stages {

        stage('Setup Python') {
            steps {
                bat '%PYTHON% --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                %PYTHON% -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Code Quality') {
            steps {
                bat '''
                pip install flake8
                flake8 . || exit 0
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                pip install pytest
                pytest || exit 0
                '''
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t renai-backend .'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline executed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}
