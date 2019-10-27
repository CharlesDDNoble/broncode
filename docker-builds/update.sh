#!/bin/bash
update_executor() {
    echo "Updating executor in $WORKDIR/$1/env"

    LOG1=`cp "$WORKDIR/executors/${1:9}executor.py" "$WORKDIR/$1/env"`
    RES=0

    LOG2=`cp "$WORKDIR/executors/codeexecutor.py" "$WORKDIR/$1/env"`
    RES=$(($RES|$?))

    if [ "$RES" -ne "0" ]
    then
        echo "\tERROR:"
        echo "\t\t$LOG1"
        echo "\t\t$LOG2"
    fi
}

update_starter() {
    echo "Updating starter in $WORKDIR/$1/env"

    LOG1=`cp "$WORKDIR/starters/start_${1:9}.py" "$WORKDIR/$1/env"`
    RES=0
    
    LOG2=`cp "$WORKDIR/starters/codeserver.py" "$WORKDIR/$1/env"`
    RES=$(($RES|$?))

    if [ "$RES" -ne "0" ]
    then
        echo "\tERROR:"
        echo "\t\t$LOG1"
        echo "\t\t$LOG2"
    fi
}

DIR_PREFIX="broncode"
WORKDIR=`pwd`

if [ ! `basename $WORKDIR` == "docker-builds" ]
then
    echo "Must be in the /docker-builds to run this script"
    exit -1
fi

for FILE in "$WORKDIR/"*
do
    FILE=`basename $FILE`
    if [ "${FILE:0:8}" == "$DIR_PREFIX" ] && [[ ! "$FILE" =~ service ]]
    then
        update_starter "$FILE"
        update_executor "$FILE"
    fi

done



rm -r tests/executors
rm -r tests/starters
cp -r starters tests/starters
cp -r executors tests/executors

echo "Updated executors and starters in tests"


exit 0