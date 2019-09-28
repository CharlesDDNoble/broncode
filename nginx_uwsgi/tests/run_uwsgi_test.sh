#!/bin/bash

# client <-> uwsgi <-> python script
echo "---------------------"
echo "Go to 127.0.0.1:8001"
echo "---------------------"
echo ""
sleep 2

# This will serve a page w/ Hello World on localhost:8001
uwsgi --http :8001 --wsgi-file test.py
