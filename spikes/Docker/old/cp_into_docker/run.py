import os
import docker
import time

def run_time_trial():
	reps = 20
	start_time = time.time()
	for i in range(0,reps):
		container = client.containers.run('test_py')	
	elapsed_time = time.time() - start_time
	elap = str(elapsed_time/reps)
	print("Average time to run container is "+elap+" sec\n")

def main():
	file_name = "hello.txt"
	client = docker.from_env()

	#create container and detach
	container = client.containers.run('test_py', detach = True)
	
	#wait until the container is running
	while "created" in container.status:
		container.reload()
	
	#TODO: get docker-py to do this...	
	#we should get docker py to do this...	
	os.system("docker cp "+file_name+" "+container.id+":/")

	#wait until the container is exited
	while "running" in container.status:
		container.reload()

	log = container.logs().decode("utf-8")
	print(log)

if __name__ == "__main__":
	main()
