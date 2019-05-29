import docker

def main():
	client = docker.from_env()
	log = client.containers.run("hello-world:latest")
	print(log.decode("utf-8"))

if __name__ == "__main__":
	main()
