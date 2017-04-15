FROM ubuntu:14.04
FROM python:2.7.13-onbuild
FROM rabbitmq

RUN apt-get update\
	&& apt-get upgrade -y\
	&& apt-get install -y\
	pika \
	twisted \
	pymongo
	

ENV RABBITMQ_USER user
ENV RABBITMQ_PASSWORD user

RUN mkdir /app
COPY . /app

EXPOSE  9000
EXPOSE  5672
EXPOSE 	27017

WORKDIR ./bin
RUN chmod +x ./server.sh
ENTRYPOINT ["./server.sh"]