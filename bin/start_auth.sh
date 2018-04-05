#!/bin/sh

echo "auth server starting"

. config/server_config.sh

if [ $IS_CONTAINER -eq 1 ]
then
echo "In container"
fi

echo $AUTH_SERVER_HOST
echo $AUTH_SERVER_PORT
echo $MASTER_SERVER_HOST
echo $MS_AUTH_QUEUE_NAME
echo $MASTER_SERVER_QUEUE_PORT

SCRIPT="-u ../src/server/auth/launch.py"
AUTH=" --host $AUTH_SERVER_HOST --port $AUTH_SERVER_PORT"
MS="--mshost $MASTER_SERVER_HOST --ms_auth_queue $MS_AUTH_QUEUE_NAME --ms_queue_port $MASTER_SERVER_QUEUE_PORT"

python $SCRIPT $AUTH $MS