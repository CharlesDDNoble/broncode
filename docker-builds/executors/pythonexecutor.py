import os
import time
import subprocess
from codeexecutor import CodeExecutor

class PythonExecutor(codeexecutor.CodeExecutor):
    
    def __init__(self):
        self._log = ""

    def run(self):
        cmd_run = ["python3", "code.py"]
        done_process = subprocess.run(
                        cmd_run, stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE)
        return(done_process)

    def execute(self):
        #TODO: create timer on compilation/run to guard against inf loop
        error_msg_run = "Something went wrong running your code:\n"

        done_process = self.run()

        #if there were errors in executing code
        if done_process.returncode:
            self._log += error_msg_run

        #add the logs of the returned process to this object's log
        self._log += done_process.stdout.decode("utf-8")
        self._log += done_process.stderr.decode("utf-8") 
    
    def execute(self):
        error_msg_run = "Something went wrong running your code:\n"
        msg_sucess = "Your code successfully ran, here's the output:\n"

        done_process = self.run()
        self._log += msg_sucess
            
        #add the _logs of the returned process to this object's _log
        self._log += done_process.stdout.decode("utf-8")
        self._log += done_process.stderr.decode("utf-8")

        

