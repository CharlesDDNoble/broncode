import os
import time
import subprocess
from . import codeexecutor

class PythonExecutor(codeexecutor.CodeExecutor):
	
	def __init__(self):
		self.log = ""

	def run(self):
		cmd_run = ["python3", "code.py"]
		done_process = subprocess.run(
						cmd_run, stdout = subprocess.PIPE,
						stderr = subprocess.PIPE)
		return(done_process)

	def execute(self):
		#TODO: create timer on compilation/run to guard against inf loop
		error_msg_run = "Something went wrong running your code:\n"

		#wait for code file to be copied into container
		while not os.path.exists("code.py"):
			time.sleep(0.25)
			pass

		done_process = self.run()

		#if there were errors in executing code
		if done_process.returncode:
			self.log += error_msg_run

		#add the logs of the returned process to this object's log
		self.log += done_process.stdout.decode("utf-8")
		self.log += done_process.stderr.decode("utf-8") 
			

		

