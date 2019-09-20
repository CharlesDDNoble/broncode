#!/bin/bash


docker swarm init >& /dev/null
LOG=`docker stack deploy -c docker-compose.yml broncode_service_c`

if [ "$?" -eq 0 ]
then
    echo "Stack started successfully!"
else
    echo "There was a problem starting the Stack!"
fi  