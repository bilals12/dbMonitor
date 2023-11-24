pipeline {
  agent { label 'jenkins-node-label' } // specify jenkins node label here

  parameters {
    string(name: 'email', defaultValue: 'your-email@example.com', description: 'notification email')
    string(name: 'git_repo_scripts', defaultValue: 'https://your-scripts-repo.url', description: 'git repo for scripts')
    string(name: 'git_repo_detector', defaultValue: 'https://your-detector-repo.url', description: 'git repo for detector')
    string(name: 'xml_config_path', defaultValue: 'path/to/config.xml', description: 'path to xml config')
  }

  environment {
    // define environment variables here (if needed)
    workdir = '/var/jenkins_workspace/workspace/dbMonitor'
    scriptsdir = "${workdir}/scripts"
    detectordir = "${workdir}/detector"
  }

  stages {
    stage('setup and update repos') {
      steps {
        script {
          dir(env.workdir) {
            // clone or update scripts repo
            if (!fileExists(env.scriptsdir)) {
              sh "git clone ${params.git_repo_scripts} ${env.scriptsdir}"
            } else {
              dir(env.scriptsdir) {
                sh 'git pull'
              }
            }

            // clone or update detector reppo
            if (!fileExists(env.detectordir)) {
              sh "git clone ${params.git_repo_detector} ${env.detectordir}"
            } else {
              dir(env.detectordir) {
                sh 'git pull'
              }
            }
          }
        }
      }
    }
    stage('select sprint branch') {
      steps {
        script {
          dir(env.scriptsdir) {
            // execute git_work script
            sh '/bin/bash git_work.sh'
          }
        }
      }
    }

    stage('monitor hosts') {
      steps {
        script {
          dir(env.detectordir) {
            // execute detector.py script
            String output = sh(script: "python3 detector.py ${params.xml_config_path}", returnStdout: true).trim()
            if (output.contains('DOWN')) {
              echo "DOWN host found. notify by email."
              main to: params.email, subject: "some machines are not responding to ping.", body: "details: ${env.BUILD_URL} \n\n${output}"
            }
            echo '--- recorded log ---'
            echo output
          }
        }
      }
    }
    // additional stages if needed
  }

  post {
    always {
      // actions to perform pipeline run, like cleanup
      cleanWs()
    }
    failure {
      // actions to perform if this pipeline fails
      mail to: params.email, subject: 'dbMonitor pipeline failure', body: "pipeline failed. check details at: ${env.BUILD_URL}"
    }
  }
}