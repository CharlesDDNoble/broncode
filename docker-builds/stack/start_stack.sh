#!/bin/bash


docker swarm init >& /dev/null

docker stack deploy -c docker-compose.yml broncode

if [ "$?" -eq 0 ]
then
    echo "Stack started successfully!"
else
    echo "There was a problem starting the Stack!"
fi  
