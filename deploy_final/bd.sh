#!/bin/bash

set -e
set -u

export DBHOST=localhost
export DBPORT=5432

psql \
    -X \
    -U postgres \
    -W admin \
    -d template1 \
    -h $DBHOST \
    -f ./crear_db.sql \
    --echo-all \
    --set AUTOCOMMIT=off \
    --set ON_ERROR_STOP=on \
    --set VERBOSITY=verbose \
    --set PGPASSWORD='postgres' \
    --set PGOPTIONS='--client-min-messages=warning' \

#cd ..

#sh ./scripts/Permisos.sh

echo "sql script successful"
