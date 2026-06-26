pipeline {
    agent any

    environment {
        IMAGE_NAME = "secure-cicd-django-app"
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        REGISTRY   = "docker.io/lahcennajmi"
        PATH       = "${WORKSPACE}/venv/bin:${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'mkdir -p reports'
            }
        }

        stage('Installation des dépendances') {
            steps {
                sh 'python3 -m venv venv'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Tests unitaires') {
            steps { sh 'pytest --junitxml=reports/tests.xml' }
        }

        stage('Analyse SonarQube') {
            steps {
                withSonarQubeEnv('sonarqube-server') {
                    sh "${tool 'SonarScanner'}/bin/sonar-scanner -Dsonar.projectKey=secure-cicd-django"
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Analyse Bandit (sécurité du code)') {
            steps { sh 'bandit -r . -x ./venv -f txt -o reports/bandit.txt' }
        }

        stage('Analyse OWASP Dependency-Check') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    withCredentials([string(credentialsId: 'nvd-api-key', variable: 'NVD_API_KEY')]) {
                        sh 'dependency-check.sh --scan . --format HTML --out reports/ --nvdApiKey $NVD_API_KEY'
                    }
                }
            }
        }
            
               
        stage('Build image Docker') {
            steps { sh 'docker build -t $REGISTRY/$IMAGE_NAME:$IMAGE_TAG .' }
        }

        stage('Scan Trivy') {
            steps {
                sh 'trivy image --severity CRITICAL,HIGH --exit-code 1 $REGISTRY/$IMAGE_NAME:$IMAGE_TAG'
            }
        }

        stage('Push Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $REGISTRY/$IMAGE_NAME:$IMAGE_TAG'
                }
            }
        }

        stage('Déploiement') {
            steps {
                sh 'docker rm -f django-app || true'
                sh 'docker run -d --name django-app -p 8000:8000 $REGISTRY/$IMAGE_NAME:$IMAGE_TAG'
            }
        }
    }

    post {
        always { junit 'reports/tests.xml' }
        failure { echo 'Pipeline en échec : voir les rapports SonarQube / Bandit / OWASP DC / Trivy.' }
    }
}
