import os
import docker
import time

class CodeHandler:

    def __init__(self, code = 0, code_file_name = 0, image_name = 0):
        #TODO: consider logging inputs and outputs
        self.code_file_name = code_file_name
        self.image_name = image_name
        self.code = code
        self.write_to_file()
        self.log = self.handle_container()
        self.clean_up()

    def handle_container(self):
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
        while "running" in container.status:
            container.reload()

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