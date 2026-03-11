pipeline {
    agent any
    
    environment {
        PROJECT_NAME = 'RenAI'
        PYTHON_VERSION = '3.9'
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE = 'renai-api'
        GCP_PROJECT = 'renai-project'
        AZURE_WEBAPP = 'renai-api'
    }
    
    tools {
        python 'python3.9'
        docker 'latest'
    }
    
    parameters {
        choice(
            name: 'DEPLOY_ENV',
            choices: ['dev', 'staging', 'prod'],
            description: 'Deployment environment'
        )
        booleanParam(
            name: 'RUN_TESTS',
            defaultValue: true,
            description: 'Run test suite?'
        )
        booleanParam(
            name: 'TRAIN_MODELS',
            defaultValue: false,
            description: 'Retrain ML models?'
        )
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/YOUR_USERNAME/RenAI-Companion.git'
                echo "✅ Checkout complete"
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-cov pylint black
                '''
                echo "✅ Environment setup complete"
            }
        }
        
        stage('Code Quality') {
            when {
                expression { params.RUN_TESTS }
            }
            steps {
                sh '''
                    . venv/bin/activate
                    black --check .
                    flake8 . --count --statistics
                    pylint --fail-under=8.0 backend/ ml_pipeline/
                '''
                echo "✅ Code quality checks passed"
            }
        }
        
        stage('Unit Tests') {
            when {
                expression { params.RUN_TESTS }
            }
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v --junitxml=test-results.xml --cov=./ --cov-report=xml
                '''
                echo "✅ All tests passed"
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
        
        stage('ML Pipeline') {
            when {
                expression { params.TRAIN_MODELS }
            }
            stages {
                stage('Data Validation') {
                    steps {
                        sh '''
                            . venv/bin/activate
                            dvc pull || true
                            python ml_pipeline/src/validate_data.py
                        '''
                    }
                }
                
                stage('Feature Engineering') {
                    steps {
                        sh '''
                            . venv/bin/activate
                            python ml_pipeline/src/features/build_features.py
                        '''
                    }
                }
                
                stage('Model Training') {
                    parallel {
                        stage('Train Churn Model') {
                            steps {
                                sh '''
                                    . venv/bin/activate
                                    python ml_pipeline/src/models/train_churn.py \
                                        --experiment "jenkins-${BUILD_NUMBER}"
                                '''
                            }
                        }
                        stage('Train Recommender') {
                            steps {
                                sh '''
                                    . venv/bin/activate
                                    python ml_pipeline/src/models/train_recommender.py \
                                        --experiment "jenkins-${BUILD_NUMBER}"
                                '''
                            }
                        }
                        stage('Train Anomaly') {
                            steps {
                                sh '''
                                    . venv/bin/activate
                                    python ml_pipeline/src/models/train_anomaly.py \
                                        --experiment "jenkins-${BUILD_NUMBER}"
                                '''
                            }
                        }
                    }
                }
                
                stage('Model Evaluation') {
                    steps {
                        sh '''
                            . venv/bin/activate
                            python ml_pipeline/src/evaluate_models.py \
                                --threshold 0.8
                        '''
                    }
                }
                
                stage('Register Models') {
                    steps {
                        sh '''
                            . venv/bin/activate
                            python ml_pipeline/src/register_models.py \
                                --stage "${params.DEPLOY_ENV}"
                        '''
                    }
                }
            }
        }
        
        stage('Build & Package') {
            steps {
                sh '''
                    # Build Docker images
                    docker build -f docker/backend/Dockerfile -t ${DOCKER_IMAGE}:latest .
                    docker build -f docker/frontend/Dockerfile -t renai-frontend:latest ./frontend
                    
                    # Tag for registry
                    docker tag ${DOCKER_IMAGE}:latest ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER}
                '''
                echo "✅ Build complete"
            }
        }
        
        stage('Deploy to Environment') {
            when {
                expression { params.DEPLOY_ENV != 'dev' }
            }
            stages {
                stage('Deploy to GCP Vertex AI') {
                    when {
                        expression { params.DEPLOY_ENV == 'staging' }
                    }
                    steps {
                        withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY')]) {
                            sh '''
                                export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
                                python scripts/deploy/deploy_to_vertex.py \
                                    --project ${GCP_PROJECT} \
                                    --model churn_model \
                                    --version ${BUILD_NUMBER}
                            '''
                        }
                    }
                }
                
                stage('Deploy to Azure ML') {
                    when {
                        expression { params.DEPLOY_ENV == 'staging' }
                    }
                    steps {
                        withCredentials([string(credentialsId: 'azure-subscription', variable: 'AZURE_SUB')]) {
                            sh '''
                                python scripts/deploy/deploy_to_azure.py \
                                    --subscription ${AZURE_SUB} \
                                    --workspace renai-ml \
                                    --model churn_model
                            '''
                        }
                    }
                }
                
                stage('Deploy to Production') {
                    when {
                        expression { params.DEPLOY_ENV == 'prod' }
                    }
                    steps {
                        sh '''
                            # Deploy API
                            docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER}
                            
                            # Update Kubernetes
                            kubectl set image deployment/renai-api \
                                renai-api=${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER} \
                                --record
                            
                            # Wait for rollout
                            kubectl rollout status deployment/renai-api
                        '''
                        echo "✅ Production deployment complete"
                    }
                }
            }
        }
        
        stage('Smoke Tests') {
            when {
                expression { params.DEPLOY_ENV == 'prod' }
            }
            steps {
                sh '''
                    # Test API endpoints
                    curl -f http://localhost:8000/health || exit 1
                    curl -f http://localhost:8000/models/status || exit 1
                    
                    # Run smoke test suite
                    python tests/smoke_tests.py
                '''
                echo "✅ Smoke tests passed"
            }
        }
    }
    
    post {
        always {
            // Cleanup
            sh 'docker system prune -f || true'
            sh 'rm -rf venv || true'
            echo "🏁 Pipeline finished"
        }
        success {
            echo "✅ Pipeline succeeded!"
            // Send success notification
            emailext (
                to: 'team@example.com',
                subject: "Pipeline SUCCESS: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "The pipeline completed successfully. Check ${env.BUILD_URL} for details."
            )
        }
        failure {
            echo "❌ Pipeline failed!"
            // Send failure notification
            emailext (
                to: 'team@example.com',
                subject: "Pipeline FAILURE: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "The pipeline failed. Check ${env.BUILD_URL} for details."
            )
        }
    }
}