import os
import time
import subprocess
from .codeexecutor import CodeExecutor

class CExecutor(CodeExecutor):
    
    def __init__(self, code, flags, inp = ''):
        with open("code.c","w") as f:
            f.write(code)

        self.input = inp
        self.flags = flags.split()

    def run(self):
        cmd_run = ["./code"]

        done_process = subprocess.run(
                    cmd_run, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    input=bytes(self.input, "utf-8"))
        if self.input:
            cmd_run += ["<", "input.txt"]
        
        self.log_command(cmd_run)

        return done_process

    def compile(self):
        cmd_compile  = ["gcc"] + self.flags + ["-o","code","code.c"]
                
        done_process = subprocess.run(
                        cmd_compile, 
                        stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE)

        self.log_command(cmd_compile)
        
        return done_process

    def execute(self):

        self.log += "Parsing gcc flags...\n"

        self.log += "Compiling code...\n"

        done_process = self.compile()

        #if there were errors in comp
        if done_process.returncode:
            self.log += self.error_msg_comp
        else:
            self.log += "Executing program...\n"
            done_process = self.run()
            self.log += self.msg_sucess
            

        #add the _logs of the returned process to this object's _log
        self.log += done_process.stdout.decode("utf-8")
        self.log += done_process.stderr.decode("utf-8")
