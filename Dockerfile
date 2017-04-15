FROM ubuntu:14.04
FROM python:2.7.13-onbuild

RUN mkdir /app
COPY . /app

EXPOSE  9000
EXPOSE  5672
EXPOSE 	27017

RUN chmod +x ./app/bin/server.sh