#!/bin/sh

. ./set_env.sh

CONFIG_FILE="${DIR}/config/mongod.conf"

mongod --config ${CONFIG_FILE}