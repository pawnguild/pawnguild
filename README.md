## Initial setup

	git clone git@github.com:pawnguild/pawnguild.git



For ease of use, add these aliases to your ~/.bashrc file.

	alias pgup="docker-compose -f docker-compose.yml -f docker-compose.dev.yml up"
	alias pgdown="docker-compose -f docker-compose.yml -f docker-compose.dev.yml down"
	alias pgtest="docker-compose -f docker-compose.yml -f docker-compose.test.yml up --abort-on-container-exit"


## Running the pawnguild dev environment

To run the pawnguild dev environment, simply

	pgup

You can pass parameters to `docker-compose` via this command by putting them after `pgup`. For example: 

	pgup --build

Run tests locally with

	pgtest


## Viewing pawnguild and the admin page

Because of nginx listening on port 80, access your local pawnguild at `localhost` in your browser. To access the django admin in your local environment, go to `localhost/admin`, and you can login with the credentials found in `docker-compose.dev.yml`

## Populating the database

1. Obtain the `db_backup.json`, which resides on our Digital Ocean droplet `137.184.81.130`.

		scp your-user@137.184.81.130:/home/david/db_backup.json ./db_backup.json

2. Copy this file into the pawnguild service, specifically at `pawnguild/services/app/db_backup.json`
3. Build and run the local environment

		 pgup

4. Open a terminal in the django app's container

		docker exec -it app bash


5. In the docker container, run 

		python manage.py loaddata db_backup.json

6. In your terminal (not inside the container), remove `db_backup.json`. There is no further need for it

## Contributing

To contribute code, you currently need write access to the repository. Once given, checkout a new branch
off of `production` and create a pull request with any changes you make. Note that for your code to pass
the automated tests, you will need to format your code with `black`.

See https://pypi.org/project/black/ for more info on what `black` is.

Note that where you install black needs to be where your vscode runs. It is not inside the docker container.
For example, I run VS Code in Linux. I installed black in my user's python environment.
