#!/bin/bash

# Delete all containers
#docker rm $(docker ps -a -q)

# Delete all images
#docker rmi $(docker images -q)

DB_NAME_TAG="db_mongo_shop7"
echo "build ${DB_NAME_TAG}" 
docker build -t ${DB_NAME_TAG} -f mongodb.dockerfile .

AUTH_NAME_TAG="auth_shop7"
echo "build ${AUTH_NAME_TAG}" 
docker build -t ${AUTH_NAME_TAG} -f auth.dockerfile .

MS_NAME_TAG="ms_shop7"
echo "build ${MS_NAME_TAG}" 
docker build -t ${MS_NAME_TAG} -f ms.dockerfile .