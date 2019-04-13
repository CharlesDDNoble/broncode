import os
import docker
import time

class CodeHandler:

    def __init__(self, code = 0, code_file_name = 0, image_name = 0):
        #TODO: consider logging inputs and outputs
        self.code_file_name = code_file_name
        self.image_name = image_name
        self.code = code
	self.time = 0
        self.write_to_file()
        self.log = self.handle_container()
        self.clean_up()

    def handle_container(self):
	error_msg_time_out = 	"Something went wrong running your code:\n\t
				 It took too long to execute, so we stopped it!\n"
	time_out = False
        #TODO: Check returns of docker-py function calls for error
        client = docker.from_env()
	
        #create container and detach
        container = client.containers.run(self.image_name, detach = True)

        #wait until the container is running
        while "created" in container.status:
            container.reload()

        #TODO: get docker-py to do this...  
        #TODO: convert to subprocess  
        os.system("docker cp "+self.code_file_name+" "+container.id+":/")

        #wait until the container is exited
	self.time = time.time()
        while "running" in container.status and not time_out:
            container.reload()
	    if time.time() - self.time >= 3.5:
		time_out = True
	
	if time_out:
		log += error_msg_time_out
	else:
        	log = container.logs().decode("utf-8")

        return(log)

    def write_to_file(self):
        out_file = open(self.code_file_name,"w")
        out_file.write(self.code)

    def clean_up(self):
        #TODO: convert to subprocess
        os.system("rm -f "+self.code_file_name)  

    def run_time_trial(self, reps = 10):
        start_time = time.time()
        for i in range(0,reps):
            handle_container()
        elapsed_time = time.time() - start_time
        elap = str(elapsed_time/reps)
        return("Average time to run container is "+elap+" sec\n")
