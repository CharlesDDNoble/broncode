import socket
import os

def handle_requests(server):
	while True:
		clientSoc = 0
	    # accept connections
		(clientSoc, address) = server.accept()
		if clientSoc:
			data = clientSoc.recv(4096)
			inFile = open("code.c","wb");
			inFile.write(data)
			inFile.close()
			res = os.system('gcc -Wall -Werror -o code code.c >& code.out')

			if res == 0:
				os.system("./code > code.out")
			else:
				errorMsg = bytes("There was an error in compiling your code:\n",'utf-8')
				clientSoc.send(errorMsg)

			#open the out file
			outFile = open("code.out","rb");

			for line in outFile:
				clientSoc.send(line)

			break
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
