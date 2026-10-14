
pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                checkout scm
                echo 'Source code downloaded successfully'
            }
        }

        stage('Validate Project') {
            steps {
                bat 'if not exist docker-compose.yml exit /b 1'
                bat 'if not exist app\\Dockerfile exit /b 1'
                bat 'if not exist app\\index.html exit /b 1'
                bat 'if not exist healer\\Dockerfile exit /b 1'
                bat 'if not exist healer\\healer.py exit /b 1'
                echo 'Project files validated successfully'
            }
        }

        stage('Build Docker Images') {
            steps {
                bat 'docker compose build'
            }
        }

        stage('Deploy Application') {
            steps {
                bat 'docker compose up -d --remove-orphans'
            }
        }

        stage('Verify Website') {
            steps {
                bat 'curl.exe --fail --silent --show-error --retry 10 --retry-connrefused --retry-delay 2 http://localhost:8082/ -o NUL'
                echo 'Website is responding successfully'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Self-Healing System deployed'
        }

        failure {
            echo 'FAILED: Check Jenkins Console Output'
        }
    }
}
