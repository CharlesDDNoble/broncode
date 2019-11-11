#!/bin/bash
build_image() {
    cd "$1"
    NAME=`basename $1`
    echo "Building $NAME"
    docker build --tag "$NAME" .
    if [ $? -ne 0 ]
    then
        echo "ERROR: There was an error builing $NAME!"
    fi
    cd ..
}

DIR_PREFIX="broncode"
WORKDIR=`pwd`

if [ ! `basename $WORKDIR` == "docker-builds" ]
then
    echo "Must be in the /docker-builds to run this script"
    exit -1
fi

for FILE in ./*
do
    FILE=`basename $FILE`
    if [ "${FILE:0:8}" == "$DIR_PREFIX" ] && [[ ! "$FILE" =~ service ]]
    then    
        build_image "$FILE"
    fi
done
exit 0
