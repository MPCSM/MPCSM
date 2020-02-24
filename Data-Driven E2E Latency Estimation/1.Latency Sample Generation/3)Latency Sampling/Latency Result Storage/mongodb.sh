docker pull mongo
docker run --name mongo -p 27017:27017 -v $PWD/db:/data/db -d mongo:latest