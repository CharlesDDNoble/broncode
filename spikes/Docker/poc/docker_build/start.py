import os
import subprocess

def compile_and_run():
    #TODO: Docstring
	#TODO: add compile args	
    cmd_run = ["python3", "code.py"]
    done_process = subprocess.run(
                        cmd_run, stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE)
    return(done_process)


def main():
	error_msg = "Something went wrong running your code:\n"
	#TODO: create timer on compilation/wait to guard against inf loop
	#wait for code file to be copied into container
	while not os.path.exists("code.py"):
		pass

	#compile code (if necessary) and run it using a subprocess
	done_process = compile_and_run()

	#if there were no errors in comp/run code
	if done_process.returncode == 0:
		print(done_process.stdout.decode("utf-8"))
	else:
		#output error msg and stderr
		print(error_msg)
		print(done_process.stdout.decode("utf-8"))
		print(done_process.stderr.decode("utf-8"))  
	

if __name__ == "__main__":
	main()
