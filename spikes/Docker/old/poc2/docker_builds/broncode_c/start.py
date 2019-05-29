import os
import subprocess
from executors.cexecutor import CExecutor

def main():
	codex = CExecutor()
	codex.execute()
	print(codex.log)	

if __name__ == "__main__":
	main()
