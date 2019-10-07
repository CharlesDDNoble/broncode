# Setting up the Production Server for Broncode

*Dependencies:*
nginx
uwsgi
uwsgi-plugin-python3

*Install:*
sudo apt install nginx
sudo apt install uwsgi uwsgi-plugin-python3

*Design Decription:*
The production server for Broncode uses nginx as a reverse proxy for serving http requests with the Django server as a backend for scripting and database access. uWSGI is used as an interface between nginx and Django to allow each program to communicate.

*Rough Explaination:*
The design can be roughly summed up like so:
    client <-> nginx <-> uWSGI <-> Django
The nginx process will run in the background, listening on the port given in the broncode_nginx.conf file.
It will serve requests for static files located in /broncode/nginx_static. For all non static requests,
nginx passes the request to uWSGI via a unix file socket. uWSGI will then pass the request to the Django 
application which will handle all requests and access database. The uWSGI process will run the Django 
application itself, so there is no need to start the server using the ./runserver script. 

*Tutorial For Setup:*
https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html

*For Tests:*
+ setup.sh: Moves broncode_uwsgi.ini and broncode_nginx.conf into the correct areas to run the tests
+ test_uwsgi.sh: Runs the test.py script at 127.0.0.1:8001 using uwsgi. This page should say "hello world".
+ test_nginx.sh: Runs the test.py script at 127.0.0.1:8000 using nginx and uwsgi. This page should say "hello world".

*For Production:*
+ setup.sh: Moves broncode_uwsgi.ini and broncode_nginx.conf into the correct areas to run the server.

*Good To Know:*
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

*Error's We've Encountered and What _You_ Can do to Fix Them:*
**For Nginx:**
+ **Bad Gateway:** Nginx is probably having trouble connecting to uWSGI, check /var/log/nginx/error.log for the problem.
                   If its socket connections, then check the permissions of the socket.
**For uWSGI:**
+ **Module not found/Import error:** Check that all dependencies have been properly installed, especially Django related
                                     dependencies.
