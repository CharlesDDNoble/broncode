from codehandler import CodeHandler

def main():
    host = ''
    port = 4000
    flags = " -o3 \n" 

    #Testing code input with a compilation error in it
    code = "int main(int argc,char** argv){error;return 0;}\n"
    exp = "Parsing gcc flags...\n" \
          "Compiling code...\n" \
          "gcc -o3 -o code code.c\n" \
          "Something went wrong compiling your code:\n" \
          "code.c: In function 'main':\n" \
          "code.c:1:32: error: 'error' undeclared (first use in this function)\n" \
          " int main(int argc,char** argv){error;return 0;}\n" \
          "                                ^~~~~\n" \
          "code.c:1:32: note: each undeclared identifier is reported only once for each function it appears in\n"
    handler = CodeHandler(host,port,code,flags)
    handler.run()
    assert(handler.log == exp)

    #Testing code input that is correct (it should compile and run successfully)
    code = "int main(int argc,char** argv){printf(\"Hello!\\n\");return 0;}\n"
    exp =   "Parsing gcc flags...\n" \
            "Compiling code...\n" \
            "gcc -o3 -o code code.c\n" \
            "Your code successfully compiled and ran, here's the output:\n" \
            "Hello!\n"
    handler = CodeHandler(host,port,code,flags)
    handler.run()
    assert(handler.log == exp)


    #Testing code input that is an infinite loop (this should cause a timeout)
    code = "int main(int argc,char** argv){while(1);return 0;}\n"
    exp = "Something went wrong running your code:\n" \
          "It took too long to execute, so we stopped it!\n"
    handler = CodeHandler(host,port,code,flags)
    handler.run()
    assert(handler.log == exp)


if __name__ == "__main__":
    main()