pipeline {
    agent any

    environment {
        PYTHONPATH = "${WORKSPACE}"
        FLASK_APP = "app/api.py"
    }

    stages {

        stage('Unit Tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                    coverage run --branch --source=app --omit=app/__init__.py,app/api.py -m pytest --junitxml=result-unit.xml test/unit
                    mv .coverage .coverage.unit
                    '''
            
                    stash includes: '.coverage.unit', name: 'unit-coverage'
                    
                    junit 'result-unit*.xml'
                }
            }
        }

        stage('REST Tests') {
            steps {
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
                    
                    coverage run --append --branch --source=app --omit=app/__init__.py,app/api.py -m pytest --junitxml=result-rest.xml test/rest
                    mv .coverage .coverage.rest
                '''
                stash includes: '.coverage.rest', name: 'rest-coverage'
                junit 'result-rest.xml'
            }
        }

        stage('Static Analysis') {
            steps {
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

        stage('Security Analysis') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                    bandit --exit-zero -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}] {msg}"
                    '''
                    recordIssues tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')], 
                    qualityGates: [[threshold: 2, type: 'TOTAL', unstable: true], 
                    [threshold:4, type: 'TOTAL', unstable: false]]
                }
            }
        }

        stage('Coverage') {
            steps {
                script {
                    unstash 'unit-coverage'
                    unstash 'rest-coverage'
                }

                sh '''
                echo "Combining coverage results"
                coverage combine .coverage.unit .coverage.rest
                coverage report
                coverage xml

                '''

                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    cobertura coberturaReportFile: 'coverage.xml', conditionalCoverageTargets: '90,80,80', lineCoverageTargets: '95,85,85', onlyStable: false
                }
                
            }

        }

        stage('Performance'){
            steps{

                sh '''
                nohup flask run > flask.log 2>&1 &
                sleep 3
                wget -q https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.tgz
                tar -xzf jmeter/apache-jmeter-5.6.3.tgz
                '''
                sh 'apache-jmeter-5.6.3/bin/jmeter.sh -n -t jmeter/test-plan.jmx -l flask.jtl'

                perfReport sourceDataFiles: 'flask.jtl'
            }
        }

    }
}
