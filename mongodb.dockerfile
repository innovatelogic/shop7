FROM mongo

#create DB directory
RUN mkdir /app

ADD ./data/mongodb/data .
COPY ./bin/config/docker_mongod.conf ./app/docker_mongod.conf

EXPOSE 27017

#ENTRYPOINT ["/app"]
CMD ["mongod"]