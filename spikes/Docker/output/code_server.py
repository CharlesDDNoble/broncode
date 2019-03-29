import socket
import subprocess
import os

def writeCodeFile(data):
	inFile = open("code.c","wb");
	inFile.write(data)	
	inFile.close()
	
def handle_requests(server):
	errorMsg = bytes("There was an error in compiling your code:\n",'utf-8')
	# outFile = open("code.out","rb");
	# capture stdout/stderr of spawned proc
	compileCmd  = ["gcc", "-Wall", "-Werror", "-o", "code", "code.c"]
	runCmd = ["./code"]
	compProc = 0
	while True:
		clientSoc = 0
	    	# accept connections
		(clientSoc, address) = server.accept()
		if clientSoc:
			data = clientSoc.recv(4096)
			writeCodeFile(data)
			compProc = subprocess.run(compileCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			if compProc.returncode == 0:
				compProc = subprocess.run(runCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				clientSoc.send(compProc.stdout)
				clientSoc.send(compProc.stderr)
				#TODO:check for runtime error
			else:
				#output compilation error
				clientSoc.send(errorMsg)
				clientSoc.send(compProc.stderr)
				
			break
	#clean up
	os.system("rm -f code code.c code.out")
	

def main():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#using 'localhost' because we only want the connection with this machine
	server.bind(('localhost', 6666))
	server.listen(5)
	handle_requests(server)
	server.close()
	
if __name__ == "__main__":
	main()
