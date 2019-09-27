#!/bin/bash

echo "---------------------"
echo "Go to 127.0.0.1:8000"
echo "---------------------"
echo ""
sleep 2

# This will serve a page w/ Hello World on localhost:8000
uwsgi --http :8000 --wsgi-file test.py
