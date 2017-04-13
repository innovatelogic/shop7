FROM alpine:3.1
FROM python:2.7.13-onbuild

COPY go ./src/common/
COPY go ./src/server
COPY go ./src/utils

COPY go ./bin/config/server_config.sh
COPY go ./bin/server.sh

WORKDIR ./go/bin
RUN pip install -r requirements.txt

EXPOSE  9000
EXPOSE  5672
EXPOSE 	27017

CMD ["server.sh"]