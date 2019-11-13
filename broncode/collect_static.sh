#!/bin/bash

sudo rm -rf nginx_static/*

# Collect static files into a single location
# for nginx to serve them
sudo python3 ./manage.py collectstatic
