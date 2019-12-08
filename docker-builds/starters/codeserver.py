import socket
import signal
import socket
from time import time, sleep

from executors.codeexecutor import CodeExecutor

class CodeServer():

    def to_dict():
        return vars(self)

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
        
        # We initialize these here for testing purposes
        self.flags = ''
        self.code = ''
        self.num_inputs = ''
        self.inputs = []

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


    def handle_connection(self, is_test=False):
        #set up server socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self.host, self.port))
        serversocket.listen(1) # become a server socket, maximum 1 connections
        
        # The OS will assign a random open port since one is not specified
        if is_test:
            self.port = serversocket.getsockname()[1]
        
        msg = ''

        while not self.should_end:
            try:
                #block until a connection is made
                # print("waiting...")
                connection, address = serversocket.accept()
                # print("got something.")

                #get compiler flags and code, remove any null bytes from packing
                self.flags = connection.recv(self.BLOCK_SIZE).decode("utf-8").replace('\0','')
                self.code = connection.recv(self.BLOCK_SIZE).decode("utf-8").replace('\0','')
                self.num_inputs = connection.recv(self.BLOCK_SIZE).decode("utf-8").replace('\0','')

                # print("num:", num_inputs)

                self.inputs = []
                for i in range(int(self.num_inputs)):
                    self.inputs.append(connection.recv(self.BLOCK_SIZE).decode("utf-8").replace('\0',''))

                ## we'll just test whether the send/recv functionality of the server works
                if is_test:
                    for i in range(int(self.num_inputs)):
                        connection.send(self.make_block("OUTPUT_"+str(i)))
                    serversocket.close()
                    return

                #set alarm to time out in case of really long running programs
                signal.alarm(self.max_time)

                codex = self.Executor(self.code,self.flags,self.inputs)

                assert(isinstance(codex,CodeExecutor))

                codex.execute()
                
                connection.send(self.make_block(codex.compilation_log))

                for log in codex.run_logs:
                    connection.send(self.make_block(log))

                # print("done.")
            except TimeoutError:
                # print("timed out.")
                self.should_end = True
            except OSError as ose:
                # print(ose)
                self.should_end = True
            finally:
                serversocket.close()

