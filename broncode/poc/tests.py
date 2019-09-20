from django.test import TestCase
from .codehandler import CodeHandler
import socket

# Create your tests here.

class CodeHandlerTestCase(TestCase):
    def setUp(self):
        pass

    def test_make_block(self):
        handler = CodeHandler(host = '', port = 4000, code = '', flags = '')
        
        # NO MESSAGE
        inp = b''
        exp = b'\0'*handler.BLOCK_SIZE
        out = handler.make_block(inp)
        self.assertEqual(len(out),handler.BLOCK_SIZE)
        self.assertEqual(out,exp)

        # MESSAGE < BLOCK_SIZE
        inp = b'Hello'
        exp = b'Hello' + b'\0'*(handler.BLOCK_SIZE-5)
        out = handler.make_block(inp)
        self.assertEqual(len(out),handler.BLOCK_SIZE)
        self.assertEqual(out,exp)

        # MESSAGE == BLOCK_SIZE
        inp = b'A'*handler.BLOCK_SIZE
        exp = b'A'*handler.BLOCK_SIZE
        out = handler.make_block(inp)
        self.assertEqual(len(out),handler.BLOCK_SIZE)
        self.assertEqual(out,exp)

        # MESSAGE > BLOCK_SIZE
        inp = b'B'*(handler.BLOCK_SIZE+10)
        exp = b'B'*handler.BLOCK_SIZE
        out = handler.make_block(inp)
        self.assertEqual(len(out),handler.BLOCK_SIZE)
        self.assertEqual(out,exp)

    def test_code_handler(self):
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
        self.assertEqual(handler.log,exp)

        #Testing code input that is correct (it should compile and run successfully)
        code = "int main(int argc,char** argv){printf(\"Hello!\\n\");return 0;}\n"
        exp =   "Parsing gcc flags...\n" \
                "Compiling code...\n" \
                "gcc -o3 -o code code.c\n" \
                "Your code successfully compiled and ran, here's the output:\n" \
                "Hello!\n"
        handler = CodeHandler(host,port,code,flags)
        handler.run()
        self.assertEqual(handler.log,exp)


        #Testing code input that is an infinite loop (this should cause a timeout)
        code = "int main(int argc,char** argv){while(1);return 0;}\n"
        exp = "Something went wrong running your code:\n" \
              "It took too long to execute, so we stopped it!\n"
        handler = CodeHandler(host,port,code,flags)
        handler.run()
        self.assertEqual(handler.log,exp)


