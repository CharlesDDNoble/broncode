import os
import subprocess
import socket

def make_block(msg):
    return msg + "\0" * (4096-len(msg))

def main():
    #listen for code
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 4500))
    serversocket.listen(1) # become a server socket, maximum 1 connections
    msg = ''
    BLOCK_SIZE = 4096
    client_soc, address = serversocket.accept()

    for i in range(0,2):
        msg += client_soc.recv(BLOCK_SIZE).decode("utf-8")

    ind = msg.index('\n')
    print(msg[:ind])
    print(msg[ind+1:])
    client_soc.send(make_block(msg).encode("utf-8"))    
    
    client_soc.close()

if __name__ == '__main__':
        main()

