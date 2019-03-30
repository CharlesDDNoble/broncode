import socket
import subprocess
import os
	
def compile_and_run():
	#TODO: Docstring
	cmd_run = ["Rscript", "code.R"]
	done_process = subprocess.run(
						cmd_run, stdout = subprocess.PIPE,
						stderr = subprocess.PIPE)
	return(done_process)


def handle_requests(server_soc):
	#TODO: Docstring
	error_msg = bytes("There was an error in compiling/running"
					  " your code:\n",'utf-8')
	done_process = 0
	while True:
		client_soc = 0
	    # accept connections
		(client_soc, address) = server_soc.accept()
		if client_soc:
			data = client_soc.recv(4096)
			#TODO: data/input validation?
			#TODO: Parsing command line args for gcc
			inFile = open("code.R","wb");
			inFile.write(data)	
			inFile.close()
			done_process = compile_and_run()
		
			#if there were no error in comp/run code
			if done_process.returncode == 0:
				client_soc.send(done_process.stdout)
			else:
				#output error msg and stderr
				client_soc.send(error_msg)
				client_soc.send(done_process.stdout)
				client_soc.send(done_process.stderr)		
			break

	#clean up
	subprocess.run(["rm", "-f", "code.R"]);
	

def main():
	server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#using 'localhost' because we only want the connection with this machine
	server_soc.bind(('localhost', 6666))
	server_soc.listen(5)
	handle_requests(server_soc)
	server_soc.close()
	
if __name__ == "__main__":
	main()
