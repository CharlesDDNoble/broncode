import os
import subprocess
from executors.rexecutor import RExecutor

def main():
    codex = RExecutor()
    codex.execute()
    print(codex.log)    

if __name__ == "__main__":
    main()

