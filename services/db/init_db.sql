CREATE DATABASE pawnguild;

CREATE USER pawnguild WITH PASSWORD 'm4KJvXJ/iLbMLcxn47ZwZDBP0jaH+zzf'

ALTER ROLE pawnguild SET client_encoding TO 'utf8';
ALTER ROLE pawnguild SET default_transaction_isolation TO 'read committed';
ALTER ROLE pawnguild SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
