pipeline {
    agent any
    
    stages {
        stage('Build'){
            steps {
                echo "Nothing to build because it is Python!!"
            }
        }
        stage('Service') {
            steps {
                sh '''
                            echo "Installing dependencies"
                            pip install --upgrade pip
                            pip install pytest
                        '''
                sh 'echo "Launching flask"'
                sh '''
                    export PYTHONPATH=$(pwd)
                    export FLASK_APP=app/api.py
                    flask run &
                '''
                sh 'echo "Launching Wiremock"'
                sh '''
                    java -jar bin/wiremock.jar --port 9090 --root-dir ./test/wiremock/ &
                '''
                sh 'sleep 5'
		sh 'echo $WORKSPACE'
            }
        }
        stage('Tests') {
            parallel {
                stage('Unit') {
                    steps {
                        echo "Launching Unit Tests"
                        sh 'echo "Running Unit Tests"'
                        sh 'python3 -m pytest test/unit'
                    }
                }
                stage('Rest') {
                    steps {
                        sh 'echo "Running Rest Tests"'
                        sh 'python3 -m pytest test/rest'
                    }
                }
            }
        }
        stage("JUnit"){
            steps {
                echo "Stage for JUnit"
            }
        }
    }
}
    
    
