import socket
import subprocess
import os

def writeCodeFile(data):
	inFile = open("code.py","wb");
	inFile.write(data)	
	inFile.close()
	
def handle_requests(server):
	errorMsg = bytes("There was an error in compiling your code:\n",'utf-8')
	# outFile = open("code.out","rb");
	# capture stdout/stderr of spawned proc
	compileCmd  = ["python3", "code.py"]
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
				clientSoc.send(compProc.stdout)
				#TODO:check for runtime error
				clientSoc.send(compProc.stderr)
			else:
				#output compilation error
				clientSoc.send(errorMsg)
				clientSoc.send(compProc.stderr)
				
			break
	#clean up
	os.system("rm -f code.py")
	

def main():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#using 'localhost' because we only want the connection with this machine
	server.bind(('localhost', 6666))
	server.listen(5)
	handle_requests(server)
	server.close()
	
if __name__ == "__main__":
	main()
