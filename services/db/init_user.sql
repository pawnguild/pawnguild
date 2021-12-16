CREATE USER pawnguild_app WITH PASSWORD 'password';

ALTER ROLE pawnguild_app SET client_encoding TO 'utf8';
ALTER ROLE pawnguild_app SET default_transaction_isolation TO 'read committed';
ALTER ROLE pawnguild_app SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE pawnguild TO pawnguild_app;
ALTER USER pawnguild_app CREATEDB;
