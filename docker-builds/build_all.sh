#!/bin/bash
DIR_SUFFIX="broncode"

build_image() {
    cd $1
    echo "Building ${1:0}"
    ./build.sh > /dev/null
    cd ..
}

for FILE in ./*
do
    FILE=`basename $FILE`
    if [ "${FILE:0:8}" == "$DIR_SUFFIX" ] && [[ ! "$FILE" =~ service ]]
    then    
        build_image "$FILE"
    fi
done
exit 0
