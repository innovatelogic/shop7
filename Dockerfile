FROM alpine:3.1
FROM python:2.7.13-onbuild

COPY ./src/common/
COPY ./src/server
COPY ./src/utils

COPY ./bin/config/server_config.sh
COPY ./bin/server.sh

WORKDIR ./bin
RUN pip install -r requirements.txt

EXPOSE  9000
EXPOSE  5672
EXPOSE 	27017

CMD ["server.sh"]