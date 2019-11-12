import socket
import signal
import socket
from time import time, sleep

from executors.codeexecutor import CodeExecutor

class CodeServer():

    def alarm_handler(self, signum, frame):
        raise TimeoutError('Timeout!')

    def __init__(self,host,port,Executor):
        signal.signal(signal.SIGALRM, self.alarm_handler)
        self.host = host
        self.port = port
        self.Executor = Executor
        self.max_time = 10
        self.should_end = False
        self.BLOCK_SIZE = 4096 #send/recv message size

    def make_block(self,msg):
        """Creates a BLOCK_SIZE message using msg, padding it with \0 if it is too short"""
        self.BLOCK_SIZE = 4096
        has_lost_data = False
        if not isinstance(msg,bytes):
            msg = bytes(msg,"utf-8")
        if len(msg) > self.BLOCK_SIZE:
            msg = msg[:self.BLOCK_SIZE]
            has_lost_data = True
        return msg + bytes(('\0' * (self.BLOCK_SIZE-len(msg))),"utf-8")

    def handle_connection(self):
        #set up server socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self.host, self.port))
        serversocket.listen(1) # become a server socket, maximum 1 connections
        msg = ''

        while not self.should_end:
            try:
                #block until a connection is made
                print("waiting...")
                connection, address = serversocket.accept()
                print("got something.")

                #get compiler flags and code, remove any null bytes from packing
                flags = connection.recv(self.BLOCK_SIZE).decode("utf-8").replace('\0','')
                code = connection.recv(self.BLOCK_SIZE).decode("utf-8").replace('\0','')
                num_inputs = connection.recv(self.BLOCK_SIZE).decode("utf-8").replace('\0','')

                inputs = []
                for _ in range(int(num_inputs)):
                    inputs.append(connection.recv(self.BLOCK_SIZE).decode("utf-8").replace('\0',''))

                #set alarm to time out in case of really long running programs
                signal.alarm(self.max_time)

                codex = self.Executor(code,flags,inputs)

                assert(isinstance(codex,CodeExecutor))

                codex.execute()
                
                connection.send(self.make_block(codex.compilation_log))
                for log in codex.run_logs:
                    connection.send(self.make_block(log))

                print("done.")
            except TimeoutError:
                serversocket.close()
                print("timed out.")
                raise SystemExit
            except OSError as ose:
                print(ose)
                self.should_end = True
