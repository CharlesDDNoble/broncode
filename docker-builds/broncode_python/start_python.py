import os
import subprocess
from executors.pythonexecutor import PythonExecutor

def main():
    codex = PythonExecutor()
    codex.execute()
    print(codex.log)    

if __name__ == "__main__":
    main()
