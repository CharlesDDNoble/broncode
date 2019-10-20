# Docker Builds for Broncode

*Dependencies:*
docker 1.5.x

*Install:*
follow instructions [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

*Description:*
This folder contains all docker images and the associated scripts 
that they use/are used to manage them. For each language supported
by Broncode, there is a separate docker container to compile and run
the code for that language. Each image is build and run as part of a
docker service, which listens on a specified port and handles requests.
In order to simplify the process of creating containers to handle new
languages, we have generalized the process of receiving and running code into two sections: starters and executors.

**Starters**
All docker start scripts are contained in the *starters* folder, these
scripts handle the socket communication to recieve code and the timeout conditions for the docker container. 

**Executors**
The compiling/running/processing of code within a container is all handled by a CodeExecutor (an abstract class specified in 
codeexecutor.py) python object; each language should have its own 
CodeExecutor to handle the specifics of executing code for that language. 
All CodeExecutors can be found in the *executors* folder.

*Rough Docker Description:*
Docker is a platform/set of programs for developing virtual application
in isolated Docker "containers". How to set up and run a container:

1.  Pull image, a docker image is basically a vm. This will be the 
    base of the environment to run the application.
    
    `docker pull <image_name>`

2.  Write Dockerfile, a Dockerfile (Case sensitive) is a
    list of instructions to build the environment for the container
    
    `touch Dockerfile`

3.  Build docker image, this will build the image specified in the 
    Dockerfile so that replicas of the image may be spawned in containers.

    `docker build --tag <NAME> Dockerfile`

    where <NAME> is your choice in name for the image, by 
    default it will be some string of chars. <NAME> (or the 
    default) will be used to run the image.

4.  Run the image, this will spawn a new container 
    instance that will execute the start script/command specified
    in the Dockerfile

    `docker run <NAME>`


*Rough Explaination of Docker Image Design:*
Each Docker Image should be built from the base image of the OS that
the server is being run on (in this case Ubuntu 18.04). From there, 
install the compiler of your choice for the language, e.g. for C use GCC, 
by modifying the dockerfile. 

You must then specify a start script for the image to run (use the 
starter template in *starters* to build a new start script). 

You should only need to modify the start template to call the 
correct CodeExecutor for the new language. Use CExecutor as an example
to create a new CodeExecutor. 

From there, you need only create a docker-compose.yml file, which will 
configure a service to be run that handles creating replicas of the new 
image (you may use *broncode_service_c/docker-compose.yml* as a template).

*Scripts:*
These are scripts to make your life easier...

*Good to Know:*
+ If you need to modify a starter or executor, then **ONLY** modify the
  files in the *starters* or *executors* folder. The corresponding update
  script will copy these files into the appropriate places.

-- Written by Charles Noble 2019
