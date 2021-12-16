CREATE USER pawnguild_app WITH PASSWORD 'm4KJvXJ/iLbMLcxn47ZwZDBP0jaH+zzf';

ALTER ROLE pawnguild_app SET client_encoding TO 'utf8';
ALTER ROLE pawnguild_app SET default_transaction_isolation TO 'read committed';
ALTER ROLE pawnguild_app SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE pawnguild TO pawnguild_app;
