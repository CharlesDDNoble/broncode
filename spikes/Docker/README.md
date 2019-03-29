How to install:
	follow instructions [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

	
How to use docker:
	1. Pull image, a docker image is basically a vm

		docker pull <image_name>

	2. Write Dockerfile, a Dockerfile (Case sensitive) is a
	list of instructions for the docker image
	
		touch Dockerfile

	3. Build docker image, this will create a base that 
	container will spawn from
	
		docker build --tag <NAME> Dockerfile

	where <NAME> is your choice in name for the image, by 
	default it will be some string of chars. <NAME> (or the
	default) will be used to run the image.

	4. Run the image, this will spawn a new container 
	instance that will execute the commands in the Dockerfile

		docker run <NAME>


	
