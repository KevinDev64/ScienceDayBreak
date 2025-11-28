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
				sh "cd frontend && docker build -t registry.kevindev64.ru/sdb-frontend:${env.BUILD_ID}-prod -t registry.kevindev64.ru/sdb-frontend:latest-prod ."
				sh "docker push sdb-frontend:${env.BUILD_ID}-prod"
				sh "docker push sdb-frontend:latest-prod"
			}	
		}

		stage("Build backend image (master) & push") {
			steps {
				sh "cd backend && docker build -t registry.kevindev64.ru/sdb-backend:${env.BUILD_ID}-prod -t registry.kevindev64.ru/sdb-backend:latest-prod ."
				sh "docker push sdb-backend:${env.BUILD_ID}-prod"
				sh "docker push sdb-backend:latest-prod"
			}	
		}

		stage("Run updater.sh on server...") {
			steps {
				sh 'ssh root@certsirius.ru "cd ScienceDayBreak && ./updater.sh"'
			}
		}
	}
}
