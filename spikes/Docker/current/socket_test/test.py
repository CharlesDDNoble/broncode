import socket

def make_block(msg):
    return msg + "\0" * (4096-len(msg))

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost',4500))

    msg = " -o3 \n"
    msg = make_block(msg)    
    sock.send(msg.encode("utf-8"))

    msg = "int main(int argc,char** argv){printf(\"HELLO WORLD!\\n\");return 0;}\n"
    msg = make_block(msg)    
    sock.send(msg.encode("utf-8"))
    
    sock.close()
