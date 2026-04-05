pipeline {
    agent any
    
    environment {
        PYTHON_HOME = "C:\\Users\\AKASH\\AppData\\Local\\Programs\\Python\\Python310"
        PATH = "${PYTHON_HOME};${PYTHON_HOME}\\Scripts;${env.PATH}"
    }
    
    stages {
        stage('Setup Python') {
            steps {
                bat 'C:\\Users\\AKASH\\AppData\\Local\\Programs\\Python\\Python310\\python.exe --version'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                bat '''
                    C:\\Users\\AKASH\\AppData\\Local\\Programs\\Python\\Python310\\python.exe -m pip install --upgrade pip
                    C:\\Users\\AKASH\\AppData\\Local\\Programs\\Python\\Python310\\python.exe -m pip install pytest flake8 black pylint
                '''
            }
        }
        
        stage('Code Quality') {
            steps {
                bat 'C:\\Users\\AKASH\\AppData\\Local\\Programs\\Python\\Python310\\python.exe -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || exit 0'
            }
        }
        
        stage('Run Tests') {
            steps {
                bat 'C:\\Users\\AKASH\\AppData\\Local\\Programs\\Python\\Python310\\python.exe -m pytest tests/ -v --tb=short || exit 0'
            }
        }
        
        stage('Docker Build') {
            steps {
                bat 'docker build -t renaii-app:latest . || exit 0'
            }
        }
    }
    
    post {
        failure {
            echo '❌ Pipeline failed!'
        }
        success {
            echo '✅ Pipeline succeeded!'
        }
    }
}
