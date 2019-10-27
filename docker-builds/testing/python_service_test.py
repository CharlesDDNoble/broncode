from codeclient import CodeClient



def main():
    host = ''
    port = 4001
    flags = "" 


    good_code = "print(\"Hello World!\")"
    good_exp =  "python3 code.py\n" \
                "Your code successfully compiled and ran, here's the output:\n" \
                "Hello World!\n"

    # handler = CodeClient(host,port,good_code,flags)
    # handler.run()
    # print("good_code:\n"+handler.log)

    bad_code = "print(Erro World!)"
    bad_exp =   "python3 code.py\n" \
                "Something went wrong running your code:\n" \
                "  File \"code.py\", line 1\n" \
                "    print(Erro World!)\n" \
                "                   ^\n" \
                "SyntaxError: invalid syntax\n"
    flags = ""

    handler = CodeClient(host,port,bad_code,flags)
    handler.run()
    print("bad_exp:\n"+handler.log)

if __name__ == "__main__":
    main()