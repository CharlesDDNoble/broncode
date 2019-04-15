import os
import docker
import time

class CodeHandler:

	def __init__(self, code = '', flags = '', code_file_name = '', image_name = ''):
		#TODO: consider logging inputs and outputs
		self.code = code
		self.flags = flags
		self.code_file_name = code_file_name
		self.image_name = image_name
		self.log = ''
		self.time = 0

	def run(self):
		self.write_files()
		self.log = self.handle_container()
		self.clean_up()

	def handle_container(self):
		error_msg_time_out = 	"Something went wrong running your code:\n\t" \
								"It took too long to execute, so we stopped it!\n"
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
		os.system("docker cp flags.txt "+container.id+":/")

		#wait until the container is exited; interrupt if time out
		self.time = time.time()
		while "running" in container.status and not time_out:
			container.reload()
			if time.time() - self.time >= 3.5:
				time_out = True
		
		#set this object's log to the time out error msg or container's log
		if time_out:
			log = error_msg_time_out
		else:
			log = container.logs().decode("utf-8")

		return(log)

	def write_files(self):
		#write code file
		code_file = open(self.code_file_name,"w")
		code_file.write(self.code)
		code_file.close()

		#write flag file
		flag_file = open('flags.txt',"w")
		flag_file.write(self.flags)
		flag_file.close()

	def clean_up(self):
		#TODO: convert to subprocess
		os.system("rm -f "+self.code_file_name)  
		os.system("rm -f flags.txt")  

	def run_time_trial(self, reps = 10):
		start_time = time.time()
		for i in range(0,reps):
			handle_container()
		elapsed_time = time.time() - start_time
		elap = str(elapsed_time/reps)
		return("Average time to run container is "+elap+" sec\n")
