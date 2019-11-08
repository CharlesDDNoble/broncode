import os
import time
import subprocess
from .codeexecutor import CodeExecutor

class CExecutor(CodeExecutor):
    
    def __init__(self, code, flags, inputs = []):
        with open("code.c","w") as f:
            f.write(code)

        self.inputs = inputs
        self.flags = flags.split()

    def run(self):
        cmd_run = ["./code"]

        self.log_command(cmd_run)

        if len(self.inputs) > 0:
            for input in self.inputs:
                done_process = subprocess.run(
                            cmd_run, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            input=bytes(input, "utf-8"),
                            )

                run_log = ""
                run_log += done_process.stdout.decode("utf-8")
                run_log += done_process.stderr.decode("utf-8")
                self.run_logs.append(run_log)
        else:
            done_process = subprocess.run(
                        cmd_run, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        )

            self.compilation_log += done_process.stdout.decode("utf-8")
            self.compilation_log += done_process.stderr.decode("utf-8")

        return True

    def compile(self):
        cmd_compile  = ["gcc"] + self.flags + ["-o","code","code.c"]
                
        done_process = subprocess.run(
                        cmd_compile, 
                        stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE)

        self.log_command(cmd_compile)
        
        return done_process

    def execute(self):
        done_process = self.compile()

        #if there were errors in comp
        if done_process.returncode:
            self.compilation_log += self.error_msg_comp
        else:
            self.compilation_log += "Executing program...\n"
            self.run()
            self.compilation_log += self.msg_sucess
