import socket
import signal
import socket
from time import time, sleep

from executors.codeexecutor import CodeExecutor

class CodeServer():

    def alarm_handler(self, signum, frame):
        raise TimeoutError('Timeout!')

    def __init__(self,host,port,Executor,code='',flags='',num_inputs='',inputs=[]):
        signal.signal(signal.SIGALRM, self.alarm_handler)
        self.host = host
        self.port = port
        self.Executor = Executor
        self.max_time = 10
        self.should_end = False
        self.BLOCK_SIZE = 4096 #send/recv message size
        
        # for testing
        self.results_log = ''
        self.code = code
        self.flags = code
        self.inputs = inputs
        self.num_inputs = num_inputs

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

    def recv_msg(self, connection, msg='', is_test=False):
        if is_test:
            return msg
        else:
            msg = connection.recv(self.BLOCK_SIZE).decode("utf-8").replace('\0','')
        return msg

    def send_msg(self, connection, msg='', is_test=False):
        if is_test:
            self.results_log += msg
        else:
            connection.send(self.make_block(msg))

    def handle_connection(self, is_test=False):
        #set up server socket
        if not is_test:
            serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serversocket.bind((self.host, self.port))
            serversocket.listen(1) # become a server socket, maximum 1 connections

        msg = ''
        print(is_test)

        while not self.should_end:
            try:
                #block until a connection is made
                print("waiting...")
                if not is_test:
                    connection, address = serversocket.accept()
                print("got something.")

                #get compiler flags and code, remove any null bytes from packing
                flags = self.recv_msg(connection,self.flags,is_test)
                code = self.recv_msg(connection,self.code,is_test)
                num_inputs = self.recv_msg(connection,self.num_inputs,is_test)

                inputs = []
                for i in range(int(num_inputs)):
                    inputs.append(self.recv_msg(connection,self.inputs[i],is_test))

                #set alarm to time out in case of really long running programs
                signal.alarm(self.max_time)

                codex = self.Executor(code,flags,inputs)

                assert(isinstance(codex,CodeExecutor))

                codex.execute()
                
                self.send_msg(connection,codex.compilation_log,is_test)

                for log in codex.run_logs:
                    self.send_msg(connection,log,is_test)

                print("done.")
            except TimeoutError:
                serversocket.close()
                print("timed out.")
                raise SystemExit
            except OSError as ose:
                print(ose)
                self.should_end = True
