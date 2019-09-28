#!/bin/bash

sudo cp ./uwsgi_params /etc/nginx
sudo cp ./broncode_nginx.conf /etc/nginx/sites-available/
sudo rm -f /etc/nginx/sites-enabled/broncode_nginx.conf
sudo ln -s /etc/nginx/sites-available/broncode_nginx.conf /etc/nginx/sites-enabled/

#restart nginx
sudo /etc/init.d/nginx restart