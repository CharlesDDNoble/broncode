import subprocess
import abc

class CodeExecutor(abc.ABC):
    """Abstract class that all code executors should inherit from."""

    @property
    def log(self):
        """The result of executing the given code, including any error encountered"""
        return self._log
    
    @abc.abstractmethod
    def execute():
        """Executes the given code and stores it in self.log"""
        pass
