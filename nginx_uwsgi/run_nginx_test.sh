#!/bin/bash

# client <-> nginx <-> uwsgi <-> python script
echo "---------------------"
echo "Go to 127.0.0.1:8000"
echo "---------------------"
echo ""
sleep 2

# if nginx is using a web socket
uwsgi --socket :8001 --wsgi-file test.py

# if nginx is using a unix socket
# uwsgi --socket ./test.sock --wsgi-file test.py