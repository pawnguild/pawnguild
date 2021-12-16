Clone the repo

	git@github.com:pawnguild/pawnguild.git


For ease of use, add these aliases to your ~/.bashrc file.

	alias pgdev="docker-compose -f docker-compose.yml -f docker-compose.dev.yml up"

`pgdev` will run the pawnguild dev environment

Because of nginx listening on port 80, access your local pawnguild at `localhost` in your browser. To access the django admin in your local environment, go to `localhost/admin`, and you can login with the credentials found in `docker-compose.dev.yml`

Populating the database

1. Obtain the `db_backup.json`, which resides on our Digital Ocean droplet `137.184.81.130`.

	`scp your-user@137.184.81.130:/home/david/db_backup.json ./db_backup.json`

2. Copy this file into the pawnguild service, specifically at `pawnguild/services/app/db_backup.json`
3. Run `pgdev`
4. In a new terminal, run `docker exec -it app bash`
5. In the docker container, run `python manage.py loaddata db_backup.json`
6. In your terminal (not inside the container), remove `db_backup.json`. There is no further need for it
