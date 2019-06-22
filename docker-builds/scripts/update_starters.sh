#!/bin/bash
DIR_SUFFIX="broncode"

cd ..
WORKDIR=`pwd`

update_starter() {
    echo "Updating starter in $WORKDIR/$1"
    rm -r -f "$WORKDIR/$1/start_${1:9}.py"
    cp "$WORKDIR/starters/start_${1:9}.py" "$WORKDIR/$1" 
}

for FILE in "$WORKDIR/"*
do
    FILE=`basename $FILE`
    if [ "${FILE:0:8}" == "$DIR_SUFFIX" ] && [[ ! "$FILE" =~ service ]]
    then
        update_starter "$FILE"
    fi
done
exit 0
