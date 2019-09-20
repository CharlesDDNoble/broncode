import os
import time
import subprocess
from . import codeexecutor

class CExecutor(codeexecutor.CodeExecutor):
    
    def __init__(self):
        self._log = ""
        self.flags = []

    def run(self):
        cmd_run = ["./code"]
        done_process = subprocess.run(
                    cmd_run, stdout = subprocess.PIPE, 
                    stderr = subprocess.PIPE)
        
        return done_process

    def parse_flags(self):
        flag_file = open('flags.txt','r')
        args = flag_file.readline().split()
        self.flags += args
        flag_file.close()

    def compile(self):
        cmd_compile  = ["gcc"] + self.flags + ["-o","code","code.c"]

        self._log += cmd_compile[0]
        for tok in cmd_compile[1:]:
            self._log += " "+tok
        self._log += "\n"
                
        done_process = subprocess.run(
                cmd_compile, stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
        
        return done_process

    def execute(self):
        error_msg_comp = "Something went wrong compiling your code:\n"
        error_msg_run = "Something went wrong running your code:\n"
        msg_sucess = "Your code successfully compiled and ran, here's the output:\n"

        self._log += "Parsing gcc flags...\n"
        self.parse_flags()

        self._log += "Compiling code...\n"
        done_process = self.compile()

        #if there were errors in comp
        if done_process.returncode:
            self._log += error_msg_comp
        else:
            done_process = self.run()
            self._log += msg_sucess
            

        #add the _logs of the returned process to this object's _log
        self._log += done_process.stdout.decode("utf-8")
        self._log += done_process.stderr.decode("utf-8")
