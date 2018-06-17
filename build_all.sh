#!/bin/bash

# Delete all containers
#docker rm $(docker ps -a -q)

# Delete all images
#docker rmi $(docker images -q)
echo [db_mongo_shop7]------------------------------------------------------------------ 
docker build -t db_mongo_shop7 -f mongodb.dockerfile .

echo [auth_shop7]------------------------------------------------------------------ 
docker build -t auth_shop7 -f auth.dockerfile .

echo [ms_shop7]------------------------------------------------------------------ 
docker build -t ms_shop7 -f ms.dockerfile .