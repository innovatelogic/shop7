#!/bin/sh

. ./${DIR}/config/local_config.sh

DEF_LOGIN=admin	
DEF_PASS=admin

SCRIPT="-u ../src/client/launch.py --auth_host $AUTH_SERVER_HOST --auth_port $AUTH_SERVER_PORT --login $DEF_LOGIN --password $DEF_PASS"

python ${SCRIPT}