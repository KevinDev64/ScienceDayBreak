pipeline {
	agent any
	options {
		skipDefaultCheckout()
	}
	
	stages {
		stage("Cleaning before building") {
			steps {
				cleanWs()
			}
		}

		stage("Checkout SCM") {
			steps {
				checkout scm
			}
		}

		stage("Generate .env file") {
			steps {
				echo "Skipping generating(bug, issue #13)!"
			}
		}

		stage("Build frontend image (master) & push") {
			environment { 
				DOCKER_REGISTRY_CREDS = credentials("DOCKER_REGISTRY")
			}
			steps {
				script {
					docker.withRegistry("https://registry.kevindev64.ru", "DOCKER_REGISTRY") {
						def prodImage = docker.build("SDB-frontend:${env.BUILD_ID}-prod", "./frontend")
						prodImage.push()
						prodImage.push("latest-prod")
					}
				}
			}	
		}

		stage("Build backend image (master) & push") {
					environment { 
						DOCKER_REGISTRY_CREDS = credentials("DOCKER_REGISTRY")
					}
					steps {
						script {
							docker.withRegistry("https://registry.kevindev64.ru", "DOCKER_REGISTRY") {
								def prodImage = docker.build("SDB-backend:${env.BUILD_ID}-prod", "./backend")
								prodImage.push()
								prodImage.push("latest-prod")
							}
						}
					}	
				}

		stage("Run updater.sh on server...") {
			steps {
				sh 'ssh root@certsirius.ru "cd ScienceDayBreak && ./updater.sh"'
			}
		}
	}
}
