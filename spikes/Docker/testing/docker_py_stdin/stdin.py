#!/usr/bin/python3.6
import docker


def main():
	client = docker.from_env()
	container = client.containers.create('busybox')
	original_text_to_send = 'hello this is from the other side'
	soc = container.attach_socket()
	#help(soc)
	data = 0
	print("isReadable = {}\nisWriteable = {}\n".format(soc.readable(),soc.writable()))
	help(soc)
	#soc.write(original_text_to_send.encode('utf-8'))
	soc.close()
	


if __name__ == "__main__":
	main()
