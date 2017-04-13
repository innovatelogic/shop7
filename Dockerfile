FROM alpine:3.1
FROM python:2.7.13-onbuild

ADD ./src/common
ADD ./src/server
ADD ./src/utils

ADD ./bin/config/server_config.sh
ADD ./bin/server.sh

WORKDIR /bin
RUN pip install -r requirements.txt

EXPOSE  9000
EXPOSE  5672
EXPOSE 	27017

CMD ["server.sh"]