#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$PSTGRES_DB" <<-EOSQL
    CREATE USER test WITH PASSWORD 'test';
    CREATE DATABASE test;
    GRANT ALL PRIVILEGES ON DATABASE test TO test;

EOSQL
