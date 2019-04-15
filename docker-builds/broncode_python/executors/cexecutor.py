import os
import subprocess
from . import codeexecutor

class CExecutor(codeexecutor.CodeExecutor):
	
	def __init__(self):
		self.log = ""
		self.flags = []

	def run(self):
		cmd_run = ["./code"]
		done_process = subprocess.run(
					cmd_run, stdout = subprocess.PIPE, 
					stderr = subprocess.PIPE)
		return(done_process)

	def compile(self):
		cmd_compile  = ["gcc","-o","code"] + self.flags + ["code.c"]

		for tok in cmd_compile:
			self.log += " "+tok
		self.log += "\n"
                
		done_process = subprocess.run(
				cmd_compile, stdout = subprocess.PIPE,
				stderr = subprocess.PIPE)
		
		return(done_process)

	def parse_flags(self):
		flag_file = open('flags.txt','r')		
		for line in flag_file:
			args = line.split(' ')
			self.flags += args
		flag_file.close()


	def execute(self):
		#TODO: create timer on compilation/run to guard against inf loop
		error_msg_comp = "Something went wrong compiling your code:\n"
		error_msg_run = "Something went wrong running your code:\n"

		#wait for flags file
		while not os.path.exists("flags.txt"):
			pass

		self.log += "Parsing gcc flags...\n"
		self.parse_flags()

		#wait for code file to be copied into container
		while not os.path.exists("code.c"):
			pass

		self.log += "Compiling code...\n"
		done_process = self.compile()

		#if there were errors in comp
		if done_process.returncode:
			self.log += error_msg_comp
		else:
			done_process = self.run()
			#can't rely on return code
			#how to check if there were errors in running
			#self.log += error_msg_run

		#add the logs of the returned process to this object's log
		self.log += done_process.stdout.decode("utf-8")
		self.log += done_process.stderr.decode("utf-8")
