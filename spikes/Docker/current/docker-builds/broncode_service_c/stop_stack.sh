#!/bin/bash

docker stack rm broncode_service_c

if [ "$?" -eq 0 ]
then
	echo "Stack stopped successfully!"
else
	echo "There was a problem stopping the Stack!"
fi	