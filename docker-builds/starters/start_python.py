import socket
import signal
import socket
from time import time, sleep

from executors.codeexecutor import CodeExecutor
from executors.pythonexecutor import PythonExecutor

def alarm_handler(signum,frame):
    raise TimeoutError('Timeout!')

def make_block(msg):
    """Creates a BLOCK_SIZE message using msg, padding it with \0 if it is too short"""
    BLOCK_SIZE = 4096
    has_lost_data = False
    if not isinstance(msg,bytes):
        msg = bytes(msg,"utf-8")
    if len(msg) > BLOCK_SIZE:
        msg = msg[:BLOCK_SIZE]
        has_lost_data = True
    return msg + bytes(('\0' * (BLOCK_SIZE-len(msg))),"utf-8")

def main():
    #After this time elapses, the script will end and the container will exit
    max_time = 180
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(int(max_time))

    try:
        #set up server socket
        host = ''
        port = 4000
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((host, port))
        serversocket.listen(1) # become a server socket, maximum 1 connections
        msg = ''
        BLOCK_SIZE = 4096 #senc/recv message size

        #block until a connection is made
        connection, address = serversocket.accept()
        
        #reset alarm to time out in case of really long running programs
        signal.alarm(10)

        #get compiler flags and code, remove any null bytes from packing
        flags = connection.recv(BLOCK_SIZE).decode("utf-8").replace('\0','')
        code = connection.recv(BLOCK_SIZE).decode("utf-8").replace('\0','')

        #Write the code file to a file with the appropriate extension
        with open("code.py","w") as f:
            f.write(code)

        #Use the appropriate CodeExecutor to compile (if necessary)
        #and run the given code
        codex = PythonExecutor()

        assert(isinstance(codex,CodeExecutor))

        codex.execute()
        connection.send(make_block(codex.log))
    except TimeoutError:
        serversocket.close()
        raise SystemExit
    except OSError as ose:
        print(ose)
    finally:
        serversocket.close()

if __name__ == "__main__":
    main()
