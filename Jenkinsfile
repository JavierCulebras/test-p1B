pipeline {
    agent {
        label 'master'
    }

    stages {

        stage('Unit') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                    export PYTHONPATH=.
                    pytest --junitxml=result-unit.xml test/unit
                    '''
                    junit 'result*.xml'
                }
            }
        }

        stage('Coverage') {
            steps {
                sh '''
                coverage run --branch --source=app --omit=app/__init__.py,app/api.py -m pytest test/unit
                coverage xml
                '''
                cobertura coberturaReportFile: 'coverage.xml', conditionalCoverageTargets: '100,0,80', lineCoverageTargets: '100,0,90'
            }
        }
    }

}