import os

def main():
	os.system("docker build --tag test-gcc . > /dev/null");
	os.system("docker run test-gcc");

if __name__ == "__main__":
	main()
