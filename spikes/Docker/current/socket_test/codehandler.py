import os
import signal
import docker
import socket
from time import time, sleep

class CodeHandler:
    """This class defines a CodeHandler object

    Spawns docker containers in order to compile and execute code.

    Attributes:
        code (str): The code that will be executed in the docker container.
        flags (str): Compiler/Interpreter flags that the code will be executed with.
        code_file_name (str): The name of file that the code will be written to.
        log (str): The out log containing the error messages, stdout, and stderr
            generated from running the given code.
        time (float): The time it took for the container to spawn, run, and exit.
        max_time (float): The maximum time allowed to wait for container to exit.
    """

    def __init__(self, host = '', port = 4000, code = '', flags = ''):
        """Constructor for the CodeHandler class."""
        #TODO: consider logging inputs and outputs
        self.host = host
        self.port = port
        self.code = code
        self.flags = flags
        self.log = ''
        self.run_time = 0
        self.max_time = 5.0
        self.time_out = False
        self.BLOCK_SIZE = 4096

    def run(self):
        """Main driver function for the CodeHandler object"""
        self.log = self.handle_container()

    def make_block(self,msg):
        return msg + bytes('\0' * (self.BLOCK_SIZE-len(msg)),"utf-8")

    def alarm_handler(self,signum,frame):
        self.time_out = True
        raise TimeoutError('Timeout!')

    def handle_container(self):
        """Handles the socket connection to a docker container."""
        error_msg_time_out =    "Something went wrong running your code:\n" \
                                "It took too long to execute, so we stopped it!\n"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log = b''
        done = False
        signal.signal(signal.SIGALRM, self.alarm_handler)
        signal.alarm(int(self.max_time))
        while not self.time_out and not done:
            try:
                sock.connect((self.host,self.port))

                self.run_time = time()
                
                sock.send(self.make_block(self.flags))
                
                sock.send(self.make_block(self.code))
                
                log = sock.recv(self.BLOCK_SIZE).replace(b'\0',b'')

                signal.alarm(0)

                self.run_time = time() - self.run_time
                
                sock.close()
                done = True
            except TimeoutError:
                log = error_msg_time_out.encode("utf-8")
            except OSError:
                self.max_time-=1
                signal.alarm(int(self.max_time))
                continue
            except Exception as excep:
                log = bytes("Something strange occurred!\n","utf-8")
                log += bytes(str(excep),"utf-8")
                done = True
        return log

    def run_time_trial(self, reps = 10):
        """Measures the average time to handle a docker container.
    
        Spawns and executes a docker container. This process is done for
        multiple repititions. The total time to complete all the repititions
        is recorded and averaged, then returned.

        Args:
            reps (int): The number of repititions to call this objects
                run() method.

        Returns:
            float: The average time in seconds to spawn and run a docker
                container.
        """
        start_time = time()
        for i in range(0,reps):
            self.run()
        elapsed_time = time() - start_time
        return elap/reps
