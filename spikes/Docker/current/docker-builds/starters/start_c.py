import os
import subprocess
from executors.cexecutor import CExecutor
import socket

def make_block(msg):
    return msg + "\0" * (4096-len(msg))

def main():
    host = ''
    port = 4000
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    serversocket.listen(1) # become a server socket, maximum 1 connections
    msg = ''
    BLOCK_SIZE = 4096

    connection, address = serversocket.accept()

    for i in range(0,2):
        msg += connection.recv(BLOCK_SIZE).decode("utf-8")
    
    ind = msg.index('\n')

    with open("flags.txt","w") as f:
        f.write(msg[ind:])

    with open("code.c","w") as f:
        f.write(msg[ind:])

    codex = CExecutor()
    codex.execute()
    connection.send(codex.log)

if __name__ == "__main__":
    main()
