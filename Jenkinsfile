pipeline {
    agent none  // No hay un agente predeterminado, asignamos agentes específicos

    environment {
        PYTHONPATH = "${WORKSPACE}"
        FLASK_APP = "app/api.py"
    }

    stages {
        stage('Unit Tests and REST Tests') {
            stages {
                stage('Unit Tests') {
                    agent { label 'master' }
                    steps {
                        sh 'rm -f .coverage.unit .coverage.rest coverage.xml'
                        echo "Executing on agent: ${NODE_NAME}"
                        echo "Current workspace: ${WORKSPACE}"
                        sh 'whoami'
                        sh 'hostname'
                        sh '''
                            coverage run --branch --source=app --omit=app/__init__.py,app/api.py -m pytest --junitxml=result-unit.xml test/unit
                            mv .coverage .coverage.unit
                            ls
                        '''
                        stash includes: '.coverage.unit', name: 'unit-coverage'
                        junit 'result-unit*.xml'
                    }
                }

                stage('REST Tests') {
                    agent { label 'master' }
                    steps {
                        sh 'rm -f .coverage.unit .coverage.rest coverage.xml'
                        echo "Executing on agent: ${NODE_NAME}"
                        echo "Current workspace: ${WORKSPACE}"
                        sh '''
                        echo "Current node: ${NODE_NAME}"
                        echo "Workspace: ${WORKSPACE}"
                        echo "Installing dependencies"
                        echo "Launching flask"
                        nohup flask run > flask.log 2>&1 &
                        echo "Launching Wiremock"
                        nohup java -jar bin/wiremock.jar --port 9090 --root-dir ./test/wiremock/ > wiremock.log 2>&1 &
                        sleep 5
                        echo "Current node: ${NODE_NAME}"
                        echo "Workspace: ${WORKSPACE}"
                        echo "Running Rest Tests"
                        '''
                        sh '''
                            coverage run --append --branch --source=app --omit=app/__init__.py,app/api.py -m pytest --junitxml=result-rest.xml test/rest
                            mv .coverage .coverage.rest
                        '''
                        stash includes: '.coverage.rest', name: 'rest-coverage'
                        junit 'result-rest.xml'
                    }
                }
            }
        }

        stage('Static Analysis') {
            parallel {
                stage('Flake8') {
                    agent { label 'node-1' }
                    steps {
                        echo "Executing on agent: ${NODE_NAME}"
                        echo "Current workspace: ${WORKSPACE}"
                        sh 'whoami'
                        sh 'hostname'
                        sh '''
                            flake8 --exit-zero --format=pylint app > flake8.out
                        '''
                        recordIssues(
                            tools: [flake8(name: 'Flake8', pattern: 'flake8.out')],
                            qualityGates: [
                                [threshold: 8, type: 'TOTAL', unstable: true],
                                [threshold: 10, type: 'TOTAL', unstable: false]
                            ]
                        )
                    }
                }

                stage('Bandit') {
                    agent { label 'node-1' }
                    steps {
                        echo "Executing on agent: ${NODE_NAME}"
                        echo "Current workspace: ${WORKSPACE}"
                        sh 'whoami'
                        sh 'hostname'
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                rm -f bandit.out
                                bandit --exit-zero -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}] {msg}"
                            '''
                            recordIssues(
                                tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')],
                                qualityGates: [
                                    [threshold: 2, type: 'TOTAL', unstable: true],
                                    [threshold: 4, type: 'TOTAL', unstable: false]
                                ]
                            )
                        }
                    }
                }

                stage('Performance') {
                    agent { label 'node-2' }
                    steps {
                        echo "Executing on agent: ${NODE_NAME}"
                        echo "Current workspace: ${WORKSPACE}"
                        sh 'whoami'
                        sh 'hostname'
                        sh '''
                            nohup flask run > flask.log 2>&1 &
                            sleep 3
                            wget -q https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.tgz
                            tar -xzf apache-jmeter-5.6.3.tgz
                        '''
                        sh 'apache-jmeter-5.6.3/bin/jmeter.sh -n -t jmeter/test-plan.jmx -l flask.jtl'
                        perfReport sourceDataFiles: 'flask.jtl'
                    }   
                }
            }
        }
    }

    post {
        always {
            node('master') {
                cleanWs()  // Limpieza en master
            }
            node('node-1') {
                cleanWs()  // Limpieza en node-1
            }
            node('node-2') {
                cleanWs()  // Limpieza en node-2
            }
        }
    }
}
