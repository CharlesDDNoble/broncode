import os
import signal
import socket
from time import time, sleep

class CodeHandler:
    """This class defines a CodeHandler object

    Conncects via socket to docker containers in order to compile and execute code.

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
        self.max_time = 10.0
        self.conn_attempt = 0
        self.BLOCK_SIZE = 4096
        self.has_lost_data = False

    def run(self):
        """Main driver function for the CodeHandler object"""
        self.log = self.handle_connection()

    def make_block(self,msg):
        """Creates a BLOCK_SIZE message using msg, padding it with \0 if it is too short"""
        if not isinstance(msg,bytes):
            msg = bytes(msg,"utf-8")
        if len(msg) > self.BLOCK_SIZE:
            msg = msg[:self.BLOCK_SIZE]
            self.has_lost_data = True
        return msg + bytes(('\0' * (self.BLOCK_SIZE-len(msg))),"utf-8")

    def handle_connection(self):
        """Handles the socket connection to a docker container."""
        error_msg_time_out = "Something went wrong running your code:\n" \
                             "It took too long to execute, so we stopped it!\n"
        error_msg_conn = "Something went wrong trying to connect to our code server!\n" \
                         "Sorry for the inconvience, please try again later."
        # Max time on all socket blocking actions
        socket.setdefaulttimeout(self.max_time)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log = ''
        done = False

        while not done and self.conn_attempt <= 3:
            try:
                sock.connect((self.host,self.port))
                self.run_time = time()
                #TODO: handle case if message is too big.
                sock.send(self.make_block(self.flags))
                sock.send(self.make_block(self.code))
                log = sock.recv(self.BLOCK_SIZE).replace(b'\0',b'').decode("utf-8")
                #in case the server times out without sending anything
                if log == '':
                    log = error_msg_time_out
                self.run_time = time() - self.run_time
                done = True
            except socket.timeout:
                log = error_msg_time_out
                done = True
            except OSError as ose:
                self.conn_attempt += 1
                log = error_msg_conn
                log += str(ose)
                sleep(2)
            # except Exception as excep:
            #     log = "Something strange occurred!\n"
            #     log += str(excep)
            #     done = True

        sock.close()
        return log

    def run_time_trial(self, reps = 10):
        """Measures the average time to handle a docker container.

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