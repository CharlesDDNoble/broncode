import os
import time
import subprocess
from . import codeexecutor

class CExecutor(codeexecutor.CodeExecutor):
    
    def __init__(self, code, flags):
        with open("code.c","w") as f:
            f.write(code)

        self.flags = flags.split()


    def run(self):
        cmd_run = ["./code"]
        done_process = subprocess.run(
                    cmd_run, stdout = subprocess.PIPE, 
                    stderr = subprocess.PIPE)
        
        return done_process

    def compile(self):
        cmd_compile  = ["gcc"] + self.flags + ["-o","code","code.c"]

        self.log += cmd_compile[0]
        for tok in cmd_compile[1:]:
            self.log += " "+tok
        self.log += "\n"
                
        done_process = subprocess.run(
                cmd_compile, stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
        
        return done_process

    def execute(self):

        self.log += "Parsing gcc flags...\n"

        self.log += "Compiling code...\n"
        done_process = self.compile()

        #if there were errors in comp
        if done_process.returncode:
            self.log += self.error_msg_comp
        else:
            done_process = self.run()
            self.log += self.msg_sucess
            

        #add the _logs of the returned process to this object's _log
        self.log += done_process.stdout.decode("utf-8")
        self.log += done_process.stderr.decode("utf-8")
