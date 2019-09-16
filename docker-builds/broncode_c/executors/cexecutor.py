import os
import time
import subprocess
from . import codeexecutor

class CExecutor(codeexecutor.CodeExecutor):
    
    def __init__(self):
        self.log = ""
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

        self.log += cmd_compile[0]
        for tok in cmd_compile[1:]:
            self.log += " "+tok
        self.log += "\n"
                
        done_process = subprocess.run(
                cmd_compile, stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
        
        return done_process

    def execute(self):
        #TODO: create timer on compilation/run to guard against inf loop
        error_msg_comp = "Something went wrong compiling your code:\n"
        error_msg_run = "Something went wrong running your code:\n"
        msg_sucess = "Your code successfully compiled and ran, here's the output:\n"

        self.log += "Parsing gcc flags...\n"
        self.parse_flags()

        self.log += "Compiling code...\n"
        done_process = self.compile()

        #if there were errors in comp
        if done_process.returncode:
            self.log += error_msg_comp
        else:
            done_process = self.run()
            self.log += msg_sucess
            

        #add the logs of the returned process to this object's log
        self.log += done_process.stdout.decode("utf-8")
        self.log += done_process.stderr.decode("utf-8")
