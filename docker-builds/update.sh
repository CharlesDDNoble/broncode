#!/bin/bash
DIR_SUFFIX="broncode"
WORKDIR=`pwd`

update_executor() {
    rm -r -f "$WORKDIR/$1/executors"
    cp -r "$WORKDIR/executors" "$WORKDIR/$1"
    echo "Updated executors in $WORKDIR/$1"
}

update_starter() {
    rm -r -f "$WORKDIR/$1/start_${1:9}.py"
    cp "$WORKDIR/starters/start_${1:9}.py" "$WORKDIR/$1"
    cp "$WORKDIR/starters/codeserver.py" "$WORKDIR/$1"
    echo "Updated starter in $WORKDIR/$1"
}

for FILE in "$WORKDIR/"*
do
    FILE=`basename $FILE`
    if [ "${FILE:0:8}" == "$DIR_SUFFIX" ] && [[ ! "$FILE" =~ service ]]
    then
        update_starter "$FILE"
        update_executor "$FILE"
    fi
done



rm -r -f tests/executors
rm -r -f tests/starters
cp -r starters tests/starters
cp -r executors tests/executors

echo "Updated executors and starters in tests"


exit 0