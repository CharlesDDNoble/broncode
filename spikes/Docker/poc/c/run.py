import os
import docker
import time

def handle_container(file_name):
	client = docker.from_env()

	#create container and detach
	container = client.containers.run('broncode_c', detach = True)
	
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
	return(log)

def write_code_file(file_name):
	code =  "#include <stdio.h>					\n" \
			"									\n" \
			"int main(int argc, char *argv[]) {	\n" \
			"	printf(\"Hello World!\\n\");	\n" \
			"	return 0;						\n" \
			"}									\n" 
	out_file = open(file_name,"w")
	out_file.write(str(code))
	
def run_time_trial():
	reps = 20
	start_time = time.time()
	for i in range(0,reps):
		handle_container()
	elapsed_time = time.time() - start_time
	elap = str(elapsed_time/reps)
	print("Average time to run container is "+elap+" sec\n")

def main():
	#TODO: consider logging inputs and outputs
	code_file_name = "code.c"
	write_code_file(code_file_name)
	log = handle_container(code_file_name)
	print(log)
	#TODO: clean up code file

if __name__ == "__main__":
	main()
