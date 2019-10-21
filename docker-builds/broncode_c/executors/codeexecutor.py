import subprocess
import abc

class CodeExecutor(abc.ABC):
    """Abstract class that all code executors should inherit from."""

    """ Log of all messages and output of program """
    log = ""

    """ Program Compilation Error Message """
    error_msg_comp = "Something went wrong compiling your code:\n"

    """ Program Running Error Message """
    error_msg_run = "Something went wrong running your code:\n"
    
    """ Program Running Success Message """
    msg_sucess = "Your code successfully compiled and ran, here's the output:\n"

    @abc.abstractmethod
    def execute():
        """Executes the given code and stores it in self.log"""
        pass
