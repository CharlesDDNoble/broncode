from codehandler import CodeHandler

def make_block(msg):
    return msg + "\0" * (4096-len(msg))

if __name__ == "__main__":
    host = ''
    port = 4000
    flags = " -o3 \n" 
    flags = make_block(flags).encode("utf-8")
    code = "int main(int argc,char** argv){while(1);return 0;}\n"
    code = make_block(code).encode("utf-8")
    
    handler = CodeHandler(host,port,code,flags)
    handler.run()
    print(handler.log.decode("utf-8"))