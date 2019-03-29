import socket
import subprocess

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 44455              # Arbitrary non-privileged port

with open("source.c", "wb") as f:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data: break
                f.write(data)

subprocess.run(["gcc", "-o", "source", "source.c"])
# what could possibly go wrong?
subprocess.run(["./source"])