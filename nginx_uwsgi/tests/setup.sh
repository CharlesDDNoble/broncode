#!/bin/bash

BASE_DIR=`cd ../..; pwd`
NGINX_CONF="./broncode_nginx.conf"
NGINX_CONF_TEMP="./broncode_nginx_template.conf"

# Create
cat $NGINX_CONF_TEMP | sed "s,BASE_DIR,$BASE_DIR,g" >& $NGINX_CONF

# MOVING FILES
sudo cp ./uwsgi_params /etc/nginx
sudo cp ./broncode_nginx.conf /etc/nginx/sites-available/
sudo rm -f /etc/nginx/sites-enabled/broncode_nginx.conf
sudo ln -s /etc/nginx/sites-available/broncode_nginx.conf /etc/nginx/sites-enabled/

#restart nginx
sudo /etc/init.d/nginx restart