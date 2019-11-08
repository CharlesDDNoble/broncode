import os
import time
import subprocess
from .codeexecutor import CodeExecutor

class PythonExecutor(CodeExecutor):
    
    def __init__(self, code, flags, inputs = []):
        with open("code.py","w") as f:
            f.write(code)

        self.inputs = inputs
        self.flags = flags.split()

    def run(self):
        cmd_run = ["python3", "code.py"]

        self.log_command(cmd_run)

        if len(self.inputs) > 0:
            for input in self.inputs:
                done_process = subprocess.run(
                            cmd_run, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            input=bytes(input, "utf-8")
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

            if done_process.stderr:
                self.compilation_log += self.error_msg_run
            else:
                self.compilation_log += self.msg_sucess
            
            self.compilation_log += done_process.stdout.decode("utf-8")
            self.compilation_log += done_process.stderr.decode("utf-8")

        return True

    def execute(self):
        self.run()
