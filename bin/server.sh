#!/bin/sh

echo "server starting script"

. config/server_config.sh

echo $MASTER_SERVER_HOST
echo $AUTH_SERVER_PORT

echo $MASTER_SERVER_HOST
echo $MASTER_SERVER_QUEUE_PORT
echo $MS_AUTH_QUEUE_NAME
echo $MS_CLIENT_QUEUE_NAME

SCRIPT="-u ../src/server/launch.py --host $MASTER_SERVER_HOST --res $RES_FOLDER --mapping $CATEGORY_MAPPING_FILENAME"
MS_INFO="--ms_auth_queue $MS_AUTH_QUEUE_NAME --ms_client_queue $MS_CLIENT_QUEUE_NAME --ms_queue_port $MASTER_SERVER_QUEUE_PORT"
DB_PARAMS="--dbhost $DB_HOST_NAME --dbport $DB_PORT --dbname $MASTER_DB_NAME"

python $SCRIPT $MS_INFO $DB_PARAMS