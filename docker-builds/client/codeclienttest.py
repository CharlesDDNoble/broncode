from .codeclient import CodeClient
import unittest
import os

class CodeClientTest(unittest.TestCase):
    def setUp(self):
        pass

    # def test_make_block(self):
    #     handler = CodeClient(host = '', port = 4000, code = '', flags = '')
        
    #     # NO MESSAGE
    #     inp = b''
    #     exp = b'\0'*handler.BLOCK_SIZE
    #     out = handler.make_block(inp)
    #     self.assertEqual(len(out),handler.BLOCK_SIZE)
    #     self.assertEqual(out,exp)

    #     # MESSAGE < BLOCK_SIZE
    #     inp = b'Hello'
    #     exp = b'Hello' + b'\0'*(handler.BLOCK_SIZE-5)
    #     out = handler.make_block(inp)
    #     self.assertEqual(len(out),handler.BLOCK_SIZE)
    #     self.assertEqual(out,exp)

    #     # MESSAGE == BLOCK_SIZE
    #     inp = b'A'*handler.BLOCK_SIZE
    #     exp = b'A'*handler.BLOCK_SIZE
    #     out = handler.make_block(inp)
    #     self.assertEqual(len(out),handler.BLOCK_SIZE)
    #     self.assertEqual(out,exp)

    #     # MESSAGE > BLOCK_SIZE
    #     inp = b'B'*(handler.BLOCK_SIZE+10)
    #     exp = b'B'*handler.BLOCK_SIZE
    #     out = handler.make_block(inp)
    #     self.assertEqual(len(out),handler.BLOCK_SIZE)
    #     self.assertEqual(out,exp)

    # # ToDo: Set this test up to use mock object for socket connection
    # def test_run_c(self):
    #     host = ''
    #     port = 4000
    #     flags = " -o3 \n" 

    #     #Testing code input with a compilation error in it
    #     code = "int main(int argc,char** argv){error;return 0;}\n"
    #     exp = "Parsing gcc flags...\n" \
    #           "Compiling code...\n" \
    #           "gcc -o3 -o code code.c\n" \
    #           "Something went wrong compiling your code:\n" \
    #           "code.c: In function 'main':\n" \
    #           "code.c:1:32: error: 'error' undeclared (first use in this function)\n" \
    #           " int main(int argc,char** argv){error;return 0;}\n" \
    #           "                                ^~~~~\n" \
    #           "code.c:1:32: note: each undeclared identifier is reported only once for each function it appears in\n"
    #     handler = CodeClient(host,port,code,flags)
    #     handler.run()
    #     # GCC seems to use the curly quotes ‘’ instead of regular quote ''
    #     out = handler.log.replace('‘','\'').replace('’','\'')
    #     self.assertEqual(out,exp)

    #     #Testing code input that is correct (it should compile and run successfully)
    #     code = "int main(int argc,char** argv){printf(\"Hello!\\n\");return 0;}\n"
    #     exp =   "Parsing gcc flags...\n" \
    #             "Compiling code...\n" \
    #             "gcc -o3 -o code code.c\n" \
    #             "Executing program...\n" \
    #             "./code\n" \
    #             "Your code successfully compiled and ran, here's the output:\n" \
    #             "Hello!\n"
    #     handler = CodeClient(host,port,code,flags)
    #     handler.run()
    #     out = handler.log.replace('‘','\'').replace('’','\'')
    #     self.assertEqual(out,exp)

    #     #Testing code input that is an infinite loop (this should cause a timeout)
    #     code = "int main(int argc,char** argv){while(1);return 0;}\n"
    #     exp = "Something went wrong running your code:\n" \
    #           "It took too long to execute, so we stopped it!\n"
    #     handler = CodeClient(host,port,code,flags)
    #     handler.max_time = 2
    #     handler.run()
    #     out = handler.log.replace('‘','\'').replace('’','\'')
    #     self.assertEqual(out,exp)

    def test_run_python(self):
        host = ''
        port = 4001
        flags = "" 

        #Testing code input with a compilation error in it

        code =  "print(Erro World!)"
        exp =   "python3 code.py\n" \
                "Something went wrong running your code:\n" \
                "  File \"code.py\", line 1\n" \
                "    print(Erro World!)\n" \
                "                   ^\n" \
                "SyntaxError: invalid syntax\n"

        handler = CodeClient(host,port,code,flags,[])
        handler.run()
        out = handler.log
        self.assertEqual(out,exp)

        #Testing code input that is correct (it should compile and run successfully)
        code = "print(\"Hello World!\")"
        exp =  "python3 code.py\n" \
                "Your code successfully compiled and ran, here's the output:\n" \
                "Hello World!\n"
        handler = CodeClient(host,port,code,flags)
        handler.run()
        out = handler.log
        self.assertEqual(out,exp)

        #Testing code input that is an infinite loop (this should cause a timeout)
        code = "while True:\n\tpass\n"
        exp = "Something went wrong running your code:\n" \
              "It took too long to execute, so we stopped it!\n"
        handler.max_time = 2
        handler = CodeClient(host,port,code,flags)
        handler.run()
        out = handler.log.replace('‘','\'').replace('’','\'')
        self.assertEqual(out,exp)


if __name__ == '__main__':
    unittest.main()