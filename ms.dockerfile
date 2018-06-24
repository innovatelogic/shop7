FROM ubuntu:14.04
FROM micktwomey/python3.4:latest
FROM rabbitmq

MAINTAINER yura.gunko@gmail.com

RUN apt-get update\
	&& apt-get install -y\
	python-pika \
	python-twisted \
	python-pymongo


ENV IS_CONTAINER 1
ENV RABBITMQ_USER user
ENV RABBITMQ_PASSWORD user

RUN mkdir /app
COPY . /app

EXPOSE 9000 5672 27017

WORKDIR ./app/bin
RUN chmod +x ./server.sh
RUN chmod +x ./config/server_config.sh
ENTRYPOINT ["./server.sh"]