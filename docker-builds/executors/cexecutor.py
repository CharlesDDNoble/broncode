import os
import time
import subprocess
import sys
from .codeexecutor import CodeExecutor

class CExecutor(CodeExecutor):
    
    def __init__(self, code, flags, inp = ''):
        with open("code.c","w") as f:
            f.write(code)

        if inp:
            with open("input.txt","w") as f:
                f.write(code)
            self.in_file = open("input.txt","w")
        else:
            self.in_file = None

        self.flags = flags.split()


    def run(self):
        if self.in_file:
            cmd_run = ["./code", "input"]
        else:
            cmd_run = ["./code"]

        self.log_command(cmd_run)

        done_process = subprocess.run(
                    cmd_run, stdout = subprocess.PIPE, 
                    stderr = subprocess.PIPE)
        
        return done_process

    def compile(self):
        cmd_compile  = ["gcc"] + self.flags + ["-o","code","code.c"]

        self.log_command(cmd_compile)
                
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
            self.log += "Executing program...\n"
            done_process = self.run()
            self.log += self.msg_sucess
            

        #add the _logs of the returned process to this object's _log
        self.log += done_process.stdout.decode("utf-8")
        self.log += done_process.stderr.decode("utf-8")
