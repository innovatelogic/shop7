#!/bin/bash

docker stop $(docker ps -a -q)

# docker stop $(docker ps -a -q)
# --entrypoint=/bin/bash

DB_NAME_TAG="db_mongo_shop7"
echo "running ${DB_NAME_TAG} ..." 
docker run -ti -d --net=host ${DB_NAME_TAG} 

AUTH_NAME_TAG="auth_shop7"
echo "running ${AUTH_NAME_TAG} ..." 
docker run -ti --entrypoint=/bin/bash --net=host ${AUTH_NAME_TAG}

MS_NAME_TAG="ms_shop7"
echo "running ${MS_NAME_TAG} ..." 
docker run -ti --net=host  ${MS_NAME_TAG}