properties([
  buildDiscarder(logRotator(numToKeepStr: '3')),
  disableConcurrentBuilds(),
])

library identifier: 'gitflowEnablers_multi@master', retriever: modernSCM([$class: 'GitSCMSource',
  remote: 'https://pscode.lioncloud.net/psinnersource/devsecops/simplified-pipelines-for-jenkins/gitflowEnablers_multi.git',
  credentialsId: 'gitlabtoken'])


library identifier: 'build-nodejs_nix@master', retriever: modernSCM([$class: 'GitSCMSource',
   remote: 'https://pscode.lioncloud.net/psinnersource/devsecops/simplified-pipelines-for-jenkins/build-nodejs_nix.git',
   credentialsId: 'gitlabtoken'])

library identifier: 'build-DockerImage@master',retriever: modernSCM([$class: 'GitSCMSource',
	remote: 'https://pscode.lioncloud.net/psinnersource/devsecops/simplified-pipelines-for-jenkins/build-DockerImage.git',
	credentialsId: 'gitlabtoken'])

library identifier: 'notfications_multi@master', retriever: modernSCM([$class: 'GitSCMSource',
        remote: 'https://pscode.lioncloud.net/psinnersource/devsecops/simplified-pipelines-for-jenkins/notifications_multi.git',
        credentialsId: 'gitlabtoken'])

library identifier: 'helm-charts_nix@helm-test',retriever: modernSCM([$class: 'GitSCMSource',
	remote: 'https://pscode.lioncloud.net/engineering-community/devops/simplified-pipelines-for-jenkins/helm-charts_nix.git',
	credentialsId: 'gitlabtoken'])

def tokens = "${env.JOB_NAME}".tokenize('/')
def branchName = tokens[tokens.size()-1].replace("%2F","-")
def (value1, shortBranch) = "${branchName}".tokenize( '-' )
branchName = env.BRANCH_NAME == "master" ? "master" : "${shortBranch}"
if(branchName != "master") {branchName = env.BRANCH_NAME == "develop" ? "develop" : "${shortBranch}"}
if(branchName != "develop" && branchName != "master") {branchName = env.BRANCH_NAME == "omni" ? "omni" : "${shortBranch}"}
def cloudEnv = env.BRANCH_NAME == "master" ? "prodcluster" : "kubernetes"
def finalBranchName = env.CHANGE_BRANCH ?: env.BRANCH_NAME
print(branchName)

pipeline {

   // options { timestamps() }

    environment{
            PROJECT_NAME = 'psi-genai-embedder'
            VERSION = '1.0.0'
            NAMESPACE = 'ps-innersource'
            RELEASE_NAME = 'psi-genai-embedder-1.0'
            gitWorkFlow = ''
            registry= 'psregistry.pscloudhub.com'
            tag = "${branchName}-${BUILD_NUMBER}"
            BRANCH_NAME = "${branchName}"
            FINAL_BRANCH_NAME = "${finalBranchName}"
    }

    agent {
        kubernetes {
            cloud "${cloudEnv}"
            inheritFrom "iris-pwa-${UUID.randomUUID().toString()}"
            yaml """
                apiVersion: v1
                kind: Pod
                metadata:
                  labels:
                    jenkins: jenkins-pipeline
                spec:
                  volumes:
                  - name: docker-sock
                    hostPath:
                      path: /var/run/docker.sock
                  - name: psregistry
                    projected:
                      sources:
                      - secret:
                          name: psregistry-creds
                          items:
                            - key: .dockerconfigjson
                              path: config.json
                  containers:
                  - name: docker
                    image: docker
                    command:
                    - cat
                    tty: true
                    volumeMounts:
                    - mountPath: /var/run/docker.sock
                      name: docker-sock
                    resources:
                      requests:
                        memory: "64Mi"
                      limits:
                        memory: "128Mi"
                  - name: kaniko
                    image: psregistry.pscloudhub.com/tools/kaniko:latest
                    imagePullPolicy: Always
                    command:
                    - /busybox/cat
                    tty: true
                    volumeMounts:
                    - name: psregistry
                      mountPath: /kaniko/.docker
                    resources:
                      requests:
                        memory: "512Mi"
                      limits:
                        memory: "1024Mi"
                  - name: kube-tools
                    image: psregistry.pscloudhub.com/tools/kube-tools:helm3
                    imagePullPolicy: Always
                    command:
                    - cat
                    tty: true
                    volumeMounts:
                    - mountPath: /var/run/docker.sock
                      name: docker-sock
                    resources:
                      requests:
                        memory: "64Mi"
                      limits:
                        memory: "128Mi"
            """
        }
    }

    stages {
      
       
        /*stage ('Unit Test') {
          steps{
            container('java-build-tools') {
              runUnitTest(archType: 'Java', buildTool: 'maven')
            }
          }
        }

           stage('Trufflehog Full Secret Scan') {
              steps {
                container('trufflehog') {
                  echo "------------------Running Repo Scan-------------------"

                  withCredentials([usernamePassword(credentialsId: 'gitlabtoken', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
                    sh '''
                      # Configure Git credentials
                      git config --global credential.username "${USERNAME}"
                      git config --global credential.helper "!f() { echo password=${PASSWORD}; }; f"
                      echo ${FINAL_BRANCH_NAME}
                      # Clone the GitLab repository
                      git clone -b main https://pscode.lioncloud.net/psinnersource_platform/psi-gpt-chatbot-service.git Platform-GPT-Chatbot-Service
                      # Clone the centralized trivy-secret repository
                     git clone -b main https://pscode.lioncloud.net/psinnersource_platform/centralized_trufflehog_scan.git trufflesecretConfig
                      echo "-----------------------Secret scan-------------------------------------"
        			   # Run trufflehog scan
                   trufflehog --debug --json filesystem Platform-GPT-Chatbot-Service --config trufflesecretConfig/user_defined_secret_config.yaml >>  trufflehog_fullscanoutput.json
                      '''
                      archiveArtifacts artifacts: 'trufflehog_fullscanoutput.json'                      
                  }
                }
              }
            }
            stage('Trufflehog Recent Introduced Secret Scan') {
              steps {
                container('trufflehog') {
                  echo "------------------Running Repo Scan-------------------"

                  withCredentials([usernamePassword(credentialsId: 'gitlabtoken', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
                    sh '''
                      # Configure Git credentials
                      git config --global credential.username "${USERNAME}"
                      git config --global credential.helper "!f() { echo password=${PASSWORD}; }; f"
                      echo "-----------------------Repo branch secret scan-------------------------------------"
                      trufflehog --debug --json git  https://pscode.lioncloud.net/psinnersource_platform/psi-gpt-chatbot-service.git --branch=main --max-depth=1 --config trufflesecretConfig/user_defined_secret_config.yaml > currentChangeScan.json

                      '''
                      script {
                      if (fileExists('currentChangeScan.json') && readFile('currentChangeScan.json').trim().length() > 0) {
                        // Archive renamed TruffleHog scan results as artifacts
                        archiveArtifacts artifacts: "currentChangeScan.json", fingerprint: true, onlyIfSuccessful: false, allowEmptyArchive: true
                        error("new secret leak injected.")
                      }
                      }
                  }
                }
              }
            }
        stage('Git Leaks Scan') {
            steps {
                container('gitleaks') {		
                script {
                     def outputFileGitLeaks = "git_leaks_results.json"
                      def customRepoName = "Platform-GPT-Chatbot-Service"
                     try{                  
                   
                    // Execute the git grep command and store the output in the file                   
                    def gitleaksCommand = """ gitleaks detect -s=${customRepoName} -r=${outputFileGitLeaks} --no-git"""

                    // Run the command
                    sh gitleaksCommand
                    //def outputFilePath="${customRepoName}/${outputFile}"   
                   
                     } catch (Exception e) {
                       echo "Gitleaks returned a non-zero exit code, but continuing the pipeline."
                       if (fileExists(outputFileGitLeaks) && readFile(outputFileGitLeaks).trim().length() > 0) {
					// Rename the artifact with the repository name
                    sh "mv ${outputFileGitLeaks} gitleaks_${outputFileGitLeaks}"

                    // Archive renamed TruffleHog scan results as artifacts
                    archiveArtifacts artifacts: "gitleaks_${outputFileGitLeaks}", fingerprint: true, onlyIfSuccessful: false, allowEmptyArchive: true
					
                    }
                  }
                }
              }
            }
        }
      stage('Git Grep Scan') {
            steps {               	
                script {
                   withCredentials([usernamePassword(credentialsId: 'gitlabtoken', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
                    sh '''
                      # Configure Git credentials
                      git config --global credential.username "${USERNAME}"
                      git config --global credential.helper "!f() { echo password=${PASSWORD}; }; f"
                      echo ${FINAL_BRANCH_NAME}
                      # Clone the GitLab repository
                      git clone -b main https://pscode.lioncloud.net/psinnersource_platform/psi-gpt-chatbot-service.git gitgrep
                     '''
                   }
                      def customRepoName = "gitgrep"
                     def repo_mail_config = readJSON file: 'trufflesecretConfig/repo_mail_config.json' 
                      def grepCustomKeywords= repo_mail_config.customKeywords
                      //git grep scan started
                    def outputFile = "git_grep_results.txt"
                    def outputFilePath=""
                    def patternComments = [
                                    "\\b(${grepCustomKeywords})\\b":"***************Below section contains exact Restricted Keyword match***************",
                                    "(${grepCustomKeywords})":"***************Below section other matches***************"
                                    ]
                     patternComments.each { pattern, comment ->
                        
                         // Execute the git grep command and store the output in the file                   
                    def grepCommand = """cd ${customRepoName} && git grep -E -i -n -I --color=always "${pattern}" | tee -a ${outputFile}"""
                   
                     // Run the command
                    sh grepCommand
                     outputFilePath="${customRepoName}/${outputFile}"   
                   if (fileExists(outputFilePath) && readFile(outputFilePath).trim().length() > 0) {
					  sh "echo '===================================================================================' >> ${customRepoName}/newfile.txt" 
                      sh "echo '${comment}' >> ${customRepoName}/newfile.txt"
                      sh "echo '===================================================================================' >> ${customRepoName}/newfile.txt"
                      sh "grep -vxFf ${customRepoName}/newfile.txt ${outputFilePath} >${outputFilePath}.tmp && mv ${outputFilePath}.tmp ${outputFilePath}"

                      sh "cat ${outputFilePath} >> ${customRepoName}/newfile.txt"     
                      echo "copy completed"   
                    }
                    }
                    outputFilePath="${customRepoName}/newfile.txt"
                    if (fileExists(outputFilePath) && readFile(outputFilePath).trim().length() > 0) {
                    // Rename the artifact with the repository name
                    sh "mv ${outputFilePath} ${outputFile}"                   

                    // Archive renamed TruffleHog scan results as artifacts
                    archiveArtifacts artifacts: "${outputFile}", fingerprint: true, onlyIfSuccessful: false, allowEmptyArchive: true
				                }                    
                    //git grep scan end                     
                }              
            }
        } */

        stage('kaniko: Build n Publish') {
          steps {
            container('kaniko') {
              echo "Deploying api ...."
                script {

                    //kubectl create secret docker-registry regcred --docker-server=psregistry.pscloudhub.com --docker-username=$HARBOR_USER --docker-password=$HARBOR_PASS

                    sh "/kaniko/executor --force --dockerfile `pwd`/Dockerfile --context `pwd` --destination=${registry}/psinnersource_platform/psi-genai-embedder:${tag}"
                } //container
           }
          }
        }

      /*  stage("sonarqube scan"){
          steps{
            container('sonarscanner') {
                withSonarQubeEnv('sonarqube') {
                sh '/opt/sonar-scanner/bin/sonar-scanner -Dproject.settings=pipelines/conf/sonar.properties'
                }
              }
          }
        } 

        stage(' SecurityScan ') {
          steps {
            container('trivy') {
               //sh "trivy image -f json -o results.json --severity HIGH,CRITICAL ${registry}/psinnersource_platform/psi-gpt-service:${tag}"
               //archiveArtifacts artifacts: 'results.json'
              
              sh "trivy image --exit-code 0 --severity HIGH,CRITICAL ${registry}/psinnersource_platform/psi-gpt-chatbot-service:${tag}"
          }
        }
      }*/


                stage('Helm Deploy') {
                    when {
                        anyOf {
                            branch 'develop'
                            branch 'master'
                            branch 'omni'
                        }
                    }
                  steps {
                    container('kube-tools') {
                      echo "Build and push docker image"
                          helmdeploy()
                      }
                    }
                  }

                stage('Reporting') {
                  steps {
                    container('puppeteer') {
                      //blueOceanScreenShot()
                    }
                  }
                }
}
  post {
    always {
     // emailNotify()
     sh "echo skip"
    }
  }
}

