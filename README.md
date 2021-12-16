Clone the repo

	git@github.com:pawnguild/pawnguild.git


For ease of use, add these aliases to your ~/.bashrc file.

	alias pgdev="docker-compose -f docker-compose.yml -f docker-compose.dev.yml up"

pgdev will run the pawnguild dev environment

To access the django admin in your local environment, go to localhost/admin, and you can login with the credentials found in docker-compose.dev.yml
