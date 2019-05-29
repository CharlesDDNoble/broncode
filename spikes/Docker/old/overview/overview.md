##_Docker Overview_
	+ **Docker Daemon**
		The Docker daemon (  `dockerd` ) listens for Docker API requests and
		manages Docker objects (like containers/images).
	+ **Docker Client**
		The Docker client ( `docker` ) is used to communicate with 
		the docker daemon which controls and Docker objects.
	+ **Docker Registry**
		The Docker registry stores Docker images. By default, Docker Hub
		(a public registry) is searched for images. When using `docker pull`
		and `docker run` images are pulled from your configured registry.
	+ **Docker Objects** 
		+ *Images*
			A **read-only** template with instructions for creating a 
			container. Created either from pulling from a public registry
			or through the use of a *Dockerfile*, each instruction is a 
			layer added onto the base image and as such only layers that 
			are changed are rebuilt when rebuilding an image.
		+ Container
			A runnable instance of an image controlled through the Docker 
			API. The level of isolation of a container and other 
			containers/host can be controlled (by default its relatively
			well isolated). Defined by its image and the configurations
			options provided on its creation.
	+ **Services**
		Services allow the scaling of containers across multiple Docker 
		daemons, which work together as a *swarm* with multiple *managers*
		and *workers*. By default, the service is load-balanced across all 
		worker nodes.


