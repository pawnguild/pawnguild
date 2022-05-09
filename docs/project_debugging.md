# Notes on how to debug PawnGuild problems


## Before messing with any containers
    Do not immediately docker-compose down them (this deletes them and their logs)!

    Grab `docker logs web`, `docker logs nginx`, and `docker logs postgres` into files. Grab the 3 log files out of the 
    nginx container (server, access, error). Grab the /var/log/info.log out of web.

    Backup the database. Store these logs and the db backup on your local machine... In case you tab delete the wrong volume

    If uptimerobot can find the time an error occured, it should be feasible to find the error messages in these files and move directly to the issue.


## Need to modify nginx config? 
    - Gonna have to reinstall the cert too. It's not ideal, but I had to use 2 volumes to make the certs and modified
    nginx config file persist. 
    - If you delete one of these 2 volumes, also delete the other, or it won't work.
    - Using `--no-cache` when you're rebuilding is probably necessary, or again, `docker system prune -a`

## Need to reinstall cert? 
    - Make sure to remove both cert and nginx conf volumes... because cert install modifies the nginx config
    - Use --test-cert first to get it working. You're limited to 5 real certs a week, make them count

## Database backup & recovery
Backup command:

    docker exec -t postgres  pg_dumpall -c -U postgres | gzip > tmp/dump_`date +%d-%m-%Y"_"%H_%M_%S`.gz

Extract a backup

    gunzip -k tmp/dump_09-05-2022_09_59_01.gz 

Put an extracted sql file into contaier

    cat your_dump.gz | docker exec -i postgres psql -U postgres

Reocovery Test

1. `docker-compose down`
2. Remove postgres volume: `docker volume rm pawnguild_postgres_data`
3. Start containers: `pgup`, verify no existing data
4. gunzip command, cat command
5. refresh page, see data
6. `docker-compose down`, `pgup`, data should persist with volume


## Migrating data
    - Grab the most recent db backup and migrate on it in local dev first.
        - At time of writing, I can't think of any scenario where db behaves differently on dev/prod.
        It's just the nginx/ssl stuff that's wonky. Once it's good on dev it should be good for prod
        - **Before running a data migration**, make sure current prod commit is tagged, annotate it saying
        what data it's working with.
            - Then backup the database. You'll need it in case the data migration fails on prod, and you need to roll back.
            - Restore the db, also go back to your tagged commit. 


## I'm done fixing my issue, how to get this up and running?
    - If certs/nginx were messed with, remove those 2 volumes, it's fine.
    - If data was messed with, back things up and tag commits first
    - Switch to pawnguild user, make sure `production` is checked out
    - Deploy via github. Either with a PR or go to Actions tab and deploy most recent one
    - Still screwed? `docker system prune -a`, re-deploy
