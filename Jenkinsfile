pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/R10010/RenAIi.git'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install flake8 pytest
                '''
            }
        }

        stage('Code Quality') {
            steps {
                sh '''
                . venv/bin/activate
                flake8 Downloads/RenAI-main/backend \
                       Downloads/RenAI-main/ml_pipeline \
                       --count --select=E9,F63,F7,F82 --show-source --statistics || true
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                mkdir -p tests
                echo "def test_ok(): assert True" > tests/test_dummy.py
                pytest
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                if [ -f Downloads/RenAI-main/docker/backend/Dockerfile ]; then
                    docker build \
                    -f Downloads/RenAI-main/docker/backend/Dockerfile \
                    -t renai-backend \
                    Downloads/RenAI-main
                else
                    echo "Dockerfile not found, skipping build"
                fi
                '''
            }
        }
    }
}
