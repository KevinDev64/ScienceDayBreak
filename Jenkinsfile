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
			steps {
				sh "cd frontend && docker build -t registry.kevindev64.ru/SDB-frontend:${env.BUILD_ID}-prod -t registry.kevindev64.ru/SDB-frontend:latest-prod ."
				sh 'docker push'
			}	
		}

		stage("Build backend image (master) & push") {
			steps {
				sh "cd backend && docker build -t registry.kevindev64.ru/SDB-backend:${env.BUILD_ID}-prod -t registry.kevindev64.ru/SDB-backend:latest-prod ."
				sh 'docker push'
			}	
		}

		stage("Run updater.sh on server...") {
			steps {
				sh 'ssh root@certsirius.ru "cd ScienceDayBreak && ./updater.sh"'
			}
		}
	}
}
