# Setting up the Production Server for Broncode

*Dependencies:*
nginx
uwsgi

*Install:*
sudo apt install nginx
sudo apt install uwsgi uwsgi-plugin-python3

*Design Decription:*
The production server for Broncode uses nginx as a reverse proxy for serving http requests with the Django server as a backend for scripting and database access. uWSGI is used as an interface between nginx and Django to allow each program to communicate.

*Tutorial For Setup:*
https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html

*Good To Know*
+ nginx's group is www-data
+ Probably need to add www-data to all groups that own files on the server (for permission 
  reasons).
+ It's best to use absolute paths for the nginx configuration file.
+ Do not name the folder that collects static files "static" if you placing that folder 
  in the Django project root directory (currently named  "/broncode", its the one with the runserver script)
+ Install uWSGI through apt-get along with the python3 plugin for it
+ Make sure Django is version 2.x and uWSGI is 2.0.x (you may experience ImportError in uWSGI
  otherwise)
+ Make sure uWSGI is running python3 (otherwise it may use python2.7 to run the Django 
  scripts)
