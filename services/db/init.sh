#!/bin/sh

psql --command "CREATE DATABASE $DB_NAME;"

psql --command "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 
psql --command "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME to $DB_USER;"

psql --command "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
psql --command "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
psql --command "ALTER ROLE $DB_USER SET timezone TO 'UTC';"

psql --command "ALTER USER $DB_USER CREATEDB;"
