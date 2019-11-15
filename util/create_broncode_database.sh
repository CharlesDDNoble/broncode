#!/bin/bash

# this script creates the broncode database.

# prerequisites:
#   * postgresql is installed
#   * you have chosen a database password and set it in create_broncode_database.sql
#   * you must run this script as the postgres user

# make sure you're postgres
if [ "$(whoami)" != "postgres" ]; then
        echo "Script must be run as postgres user."
        exit -2
fi

# get password
echo -n "Enter a database password to create a user with: "
read -s db_password1
echo

echo -n "Re-enter password: "
read -s db_password2
echo

if [ $db_password1 != $db_password2 ]; then
    echo "Passwords don't match."
    exit -2
fi

psql \
    -X \
    -f create_broncode_database.sql \
    --echo-all \
    --set ON_ERROR_STOP=on \
    --set CHOSEN_PASSWORD=$db_password1

psql_exit_status=$?
if [ $psql_exit_status != 0 ]; then
    echo "psql failed while trying to run this sql script" 1>&2
    exit $psql_exit_status
fi

echo "database setup successful"
exit 0
