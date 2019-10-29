import os
import time
import subprocess
from .codeexecutor import CodeExecutor

class RExecutor(CodeExecutor):
    
    def __init__(self, code, flags, inp = ''):
        with open("code.r","w") as f:
            f.write(code)

        self.input = inp

        self.flags = flags.split()

    def run(self):
        cmd_run = ["Rscript", "code.r"]

        done_process = subprocess.run(
                    cmd_run, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    input=bytes(self.input,"utf-8"))
        
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

        
