import os
import time
import subprocess
from .codeexecutor import CodeExecutor

class PythonExecutor(CodeExecutor):
    def __init__(self, code, flags, inputs = []):
        with open("code.py","w") as f:
            f.write(code)

        self.run_logs = []
        self.inputs = inputs
        self.flags = flags.split()

    def run(self):
        cmd_run_base = ["python3", "code.py"]

        if len(self.inputs) > 0:
            for inp in self.inputs:
                cmd_run = cmd_run_base + inp.split()
                self.log_command(cmd_run)
                done_process = subprocess.run(
                    cmd_run, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    )

                run_log = ""
                run_log += done_process.stdout.decode("utf-8")
                run_log += done_process.stderr.decode("utf-8")
                self.run_logs.append(run_log)
        else:
            self.log_command(cmd_run_base)
            done_process = subprocess.run(
                cmd_run_base, 
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
