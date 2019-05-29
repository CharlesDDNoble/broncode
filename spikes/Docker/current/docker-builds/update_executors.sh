#!/bin/bash
DIR_SUFFIX="broncode"

update() {
        echo "Updating /executors in ${1:2}"
        rm -r -f $1/executors
        cp -r ./executors $1
}

for FILE in ./*
do
    if [ "${FILE:2:8}" == "$DIR_SUFFIX" ] && [ "${FILE:11:7}" != "service" ]
    then
        update "$FILE"
    fi
done
exit 0
