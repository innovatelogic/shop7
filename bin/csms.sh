#!/bin/sh

. ./set_env.sh

. ${DIR}/config/server_config.sh

INPUT="${DIR}../data/"

SCRIPT="-u ${DIR}/../src/cmsc/launcher.py"
DB_PARAMS="--dbhost ${DB_HOST_NAME} --dbport ${DB_PORT} --dbname ${MASTER_DB_NAME}"
PARAMS="--input ${INPUT}"

python ${SCRIPT} ${PARAMS} ${DB_PARAMS}