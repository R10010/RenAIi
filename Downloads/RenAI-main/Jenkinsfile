pipeline {
    agent any
    
    parameters {
        choice(name: 'TRAIN_MODEL', choices: ['emotion', 'churn', 'gesture'], description: 'Model to train')
        string(name: 'EXPERIMENT_NAME', defaultValue: 'jenkins-run', description: 'MLflow experiment name')
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/YOUR_USERNAME/RenAI.git'
            }
        }
        stage('Setup') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\pip install -r requirements.txt'
            }
        }
        stage('Train Model') {
            steps {
                bat "venv\\Scripts\\python ml_pipeline/src/models/train_${params.TRAIN_MODEL}.py --experiment ${params.EXPERIMENT_NAME}"
            }
        }
        stage('Register Model') {
            steps {
                bat "venv\\Scripts\\python scripts/register_model.py --model ${params.TRAIN_MODEL} --run-id ${env.BUILD_NUMBER}"
            }
        }
    }
}