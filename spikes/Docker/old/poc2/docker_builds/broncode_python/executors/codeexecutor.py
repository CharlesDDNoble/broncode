import subprocess
import abc

class CodeExecutor(abc.ABC):
    @property
    def get_log(self):
        return self.log
    

    @abc.abstractmethod
    def execute():
        pass
