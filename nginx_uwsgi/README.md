# Setting up the Production Server for Broncode

*Dependencies:*
nginx
uwsgi

*Design Decription*
The production server for Broncode uses nginx as a reverse proxy for serving http requests with the Django server as a backend for scripting and database access. uWSGI is used as an interface between nginx and Django to allow each program to communicate.

*Tutorial For Setup:*
https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html