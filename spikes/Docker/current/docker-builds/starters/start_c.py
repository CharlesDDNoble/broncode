from executors.cexecutor import CExecutor
import socket
import signal
import socket
from time import time, sleep

def alarm_handler(signum,frame):
        raise TimeoutError('Timeout!')

def make_block(msg):
    return msg + '\0' * (4096-len(msg))

def main():
    #Set alarm to exit program
    max_time = 60
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(int(max_time))

    try:
        #set up socket
        host = ''
        port = 4000
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((host, port))
        serversocket.listen(1) # become a server socket, maximum 1 connections
        msg = ''
        BLOCK_SIZE = 4096 #senc/recv message size

        #block until a connection is made
        connection, address = serversocket.accept()
        
        #reset alarm for 10 seconds
        signal.alarm(10)

        #get compiler flags and code, remove any null bytes from packing
        for i in range(0,2):
            msg += connection.recv(BLOCK_SIZE).decode("utf-8").replace('\0','')
        
        ind = msg.index('\n')

        with open("flags.txt","w") as f:
            f.write(msg[:ind])

        with open("code.c","w") as f:
            f.write(msg[ind:])

        codex = CExecutor()
        codex.execute()
        connection.send(bytes(codex.log,"utf-8"))
    except TimeoutError:
        serversocket.close()
        raise SystemExit
    except OSError as ose:
        print(ose)
    finally:
        serversocket.close()

if __name__ == "__main__":
    main()
