#!/bin/bash
DIR_SUFFIX="broncode"

cd ..
WORKDIR=`pwd`

update_executor() {
    echo "Updating executors in $WORKDIR/$1"
    rm -r -f "$WORKDIR/$1/executors"
    cp -r "$WORKDIR/executors" "$WORKDIR/$1"
}

for FILE in "$WORKDIR/"*
do
    FILE=`basename $FILE`
    if [ "${FILE:0:8}" == "$DIR_SUFFIX" ] && [[ ! "$FILE" =~ service ]]
    then
        update_executor "$FILE"
    fi
done
exit 0
