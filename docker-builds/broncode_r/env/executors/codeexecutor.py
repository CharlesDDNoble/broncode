import subprocess
import abc

class CodeExecutor(abc.ABC):
    """ Abstract class that all code executors should inherit from. """

    """ Log of all messages and output of program """
    compilation_log = ""
    run_logs = []

    """ Program Compilation Error Message """
    error_msg_comp = "Something went wrong compiling your code:\n"

    """ Program Running Error Message """
    error_msg_run = "Something went wrong running your code:\n"
    
    """ Program Running Success Message """
    msg_sucess = "Your code successfully compiled and ran, here's the output:\n"

    def log_command(self,command):
        """ Adds the command to run a subprocess to self.log """
        for tok in command:
            self.compilation_log += tok+" "
        self.compilation_log = self.compilation_log[0:-1]+"\n"

    @abc.abstractmethod
    def execute():
        """ Executes the given code and stores it in self.log """
        pass
