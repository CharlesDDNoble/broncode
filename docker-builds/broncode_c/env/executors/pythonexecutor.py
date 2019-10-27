import os
import time
import subprocess
from .codeexecutor import CodeExecutor

class PythonExecutor(CodeExecutor):
    
    def __init__(self, code, flags, inp = ''):
        with open("code.py","w") as f:
            f.write(code)

        if inp:
            with open("input.txt","w") as f:
                f.write(code)
            self.in_file = open("input.txt","r")
        else:
            self.in_file = None

        self.flags = flags.split()

    def run(self):
        cmd_run = ["python3", "code.py"]

        done_process = subprocess.run(
                    cmd_run, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    stdin=self.in_file)
        
        if self.in_file:
            cmd_run += ["input.txt"]
            self.in_file.close()

        self.log_command(cmd_run)

        
        return done_process

    def execute(self):
        done_process = self.run()
        if done_process.stderr:
            self.log += self.error_msg_run
        else:
            self.log += self.msg_sucess
            
        #add the _logs of the returned process to this object's _log
        self.log += done_process.stdout.decode("utf-8")
        self.log += done_process.stderr.decode("utf-8")

        

