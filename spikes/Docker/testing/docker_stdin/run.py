import os
import subprocess
import time

def main():
	cmd1 = ["docker", "create", "stdin_test"]
	proc = subprocess.run(cmd1,stdout=subprocess.PIPE)
	cont_id = proc.stdout.decode("utf-8")


	cmd2 = ["docker", "start"]
	cmd2.append(cont_id[:-1])
	subprocess.run(cmd2)

#	cmd3 = ["docker", "kill"]
#	cmd3.append(cont_id)
#	subprocess.run(cmd3)



if __name__ == "__main__":
	main()
