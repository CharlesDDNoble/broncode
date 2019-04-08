import os
import time

def main():
	while not os.path.exists("hello.txt"):
		pass
	in_file = open("hello.txt","r")
	for line in in_file:
		print(line)

if __name__ == "__main__":
	main()
