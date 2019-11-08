# Docker Builds for Broncode

*Dependencies:*
+ docker 1.5.x [see install below]
+ python3 [apt]
+ r-base [apt]
+ gcc [apt]
+ matplotlab [pip3] (only for performance testing)

*Docker Install:*
follow instructions [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

*Description:*
This folder contains all docker images and the associated scripts 
that they use/are used to manage them. For each language supported
by Broncode, there is a separate docker container to compile and run
the code for that language. Each image is build and run as part of a
docker service, which listens on a specified port and handles requests.
In order to simplify the process of creating containers to handle new
languages, we have generalized the process of receiving and running code 
into two sections: starters and executors.

**Starters**
All docker start scripts are contained in the *starters* folder, these
scripts handle the socket communication to recieve code and the timeout
conditions for the docker container. 

**Executors**
The compiling/running/processing of code within a container is all handled 
by a CodeExecutor (an abstract class specified in codeexecutor.py) python object;
each language should have its own CodeExecutor to handle the specifics of executing
code for that language. All CodeExecutors can be found in the *executors* folder.

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

*Stack:*
Each broncode image is used as the base of a service defined in ./stack/docker-compose.yml.
From this file you can update current services as well as create new services. Two self explainatory
scipts exist in this folder, start_stack.sh and stop_stack.sh. **These two scripts will sometimes fail
if the stack has been either started or stopped too quickly.** In this case just wait a couple minutes
for the docker daemon to free up or prepare the stack, then try again.

*Scripts:*
+ update.sh: Updates all the executors, starters, and codeclient.py in the /env
  folder for each of the broncode services, prefixed with "broncode".
+ build.sh: Builds each broncode docker image according to the dockerfile in its
  folder.

*Good to Know:*
+ If you need to modify a starter or executor, then **ONLY** modify the
  files in the *starters* or *executors* folder. The corresponding update
  script will copy these files into the appropriate places.

*Creating a New Service:*
For this example, let's say we want to make a new docker service that takes R code and
compiles and executes it, then returns the result.

1. Make a new executor
    To create a new executor, it may be helpful to start with a current executor
    as a template and build from there. Since R is interpreted, we'll use the 
    PythonExecutor. 
    + Copy pythonexecutor.py into a new file rexecutor.py. 
    + Open rexecutor.py and replace all instances of Python with R
    + In __init__ change "code.py" to "code.r"
        This is the code file that will be executed.
    + In __run__ in cmd_run change ["python3", "code.py"] to ["Rscript", "code.r"]
        This is the command to compile and run the given code file.
 2. Make a new starter
    To create a new starter, use starter_template.py in /starters.
    + Copy starter_template.py into a new file start_r.py. 
    + Open start_r.py and modify the first import, change "from executors.cexecutor import CExecutor"
        to "from executors.rexecutor import RExecutor".
    + In __main__ change the port to the new service's port number, in this case we use 4002
        and change the Executor from  "CExecutor" to "RExecutor"
2. Make a new docker image
    Now we need to setup the environment for the new image.
    + Make a new directory named "broncode_[LANGUANGE NAME]", i.e. "broncode_r". Note
        this convention is important for the update.sh and build.sh scripts to run correctly.
    + Move into ./broncode_r and make a dockerfile, for this example its easier to copy an
        existing dockerfile from an existing service, again we use the python dockerfile.
    + Open the dockerfile, we need to make two modifications: add the compiler/interpreter of the
        chosen language and expose the correct port. Add "r-base" to the end of the __RUN__ command
        and change the Expose command's argument to 4002 (the port number of the new service). Close 
        the file.
    + Make a new directory name "env", this will be used to store all the files that should be copied
        into the container at startup.
    + Run the update.sh and build.sh scripts (in that order) and if all went correctly, the new 
        image should be built.
3. Make a new service
    + Open ./stack/docker-compose.yml
    + Copy and paste the service "python_service" along with all its fields below it as the template 
        of the service.
    + Change the name of the new service to r_service.
    + Change the name of the network to rnet and add rnet to the list of networks at the bottom 
        of the file.
    + Change the port mapping to "4002:4002".
    + Close the file and restart the stack if it is running (./stop_stack then ./start_stack) else
        start the stack (./start_stack).
    
-- Written by Charles Noble 2019
