#!/usr/bin/python3

import unittest
import executors
import client

from client.codeclient import CodeClient
import unittest
import os

class SystemTest(unittest.TestCase):
    def test_run_c(self):
        host = ''
        port = 4000
        flags = "-O3" 

        #Testing code input with a compilation error in it
        code = "int main(int argc,char** argv){error;return 0;}\n"
        exp = "gcc -O3 -o code code.c\n" \
              "Something went wrong compiling your code:\n" \
              "code.c: In function 'main':\n" \
              "code.c:1:32: error: 'error' undeclared (first use in this function)\n" \
              " int main(int argc,char** argv){error;return 0;}\n" \
              "                                ^~~~~\n" \
              "code.c:1:32: note: each undeclared identifier is reported only once for each function it appears in\n"
        handler = CodeClient(host,port,code,flags)
        handler.run()
        # GCC seems to use the curly quotes ‘’ instead of regular quote ''
        out = handler.compilation_log.replace('‘','\'').replace('’','\'')
        self.assertEqual(out,exp)

        #Testing code input that is correct (it should compile and run successfully)
        code = "int main(int argc,char** argv){printf(\"Hello!\\n\");return 0;}\n"
        exp =   "gcc -O3 -o code code.c\n" \
                "Executing program...\n" \
                "Your code successfully compiled and ran, here's the output:\n" \
                "./code\n" \
                "Hello!\n"
        handler = CodeClient(host,port,code,flags)
        handler.run()
        out = handler.compilation_log.replace('‘','\'').replace('’','\'')
        self.assertEqual(out,exp)

        #Testing code input that is an infinite loop (this should cause a timeout)
        code = "int main(int argc,char** argv){while(1);return 0;}\n"
        exp = "Something went wrong running your code:\n" \
              "It took too long to execute, so we stopped it!\n"
        handler = CodeClient(host,port,code,flags)
        handler.max_time = 2
        handler.run()
        out = handler.log.replace('‘','\'').replace('’','\'')
        self.assertEqual(out,exp)

        #Testing code input that uses command lines
        code = \
            "#include <stdio.h>\n" \
            "int main(int argc, char* argv[]) {\n" \
            "    printf(\"%s\\n\", argv[1]);\n" \
            "    return 0;\n" \
            "}\n"

        exp = "input!\n"
        handler = CodeClient(host,port,code,flags,["input!"])
        handler.run()
        out = handler.run_logs[0].replace('‘','\'').replace('’','\'')
        self.assertEqual(out,exp)

        code = \
            "#include <stdio.h>\n" \
            "int main(int argc, char* argv[]) {\n" \
            "    printf(\"%s\\n\", argv[1]);\n" \
            "    printf(\"%s\\n\", argv[2]);\n" \
            "    return 0;\n" \
            "}\n"

        exp = "input!\noutput!\n"
        handler = CodeClient(host,port,code,flags,["input! output!"])
        handler.run()
        out = handler.run_logs[0].replace('‘','\'').replace('’','\'')
        self.assertEqual(out,exp)

    def test_run_python(self):
        host = ''
        port = 4001
        flags = "" 

        # Testing code input with a compilation error in it
        code =  "print(Erro World!)"
        exp =   "python3 code.py\n" \
                "Something went wrong running your code:\n" \
                "  File \"code.py\", line 1\n" \
                "    print(Erro World!)\n" \
                "                   ^\n" \
                "SyntaxError: invalid syntax\n"

        handler = CodeClient(host,port,code,flags,[])
        handler.run()
        out = handler.compilation_log
        self.assertEqual(out,exp)

        #Testing code input that is correct (it should compile and run successfully)
        code = "print(\"Hello World!\")"
        exp =  "python3 code.py\n" \
                "Your code successfully compiled and ran, here's the output:\n" \
                "Hello World!\n"
        handler = CodeClient(host,port,code,flags)
        handler.run()
        out = handler.compilation_log
        self.assertEqual(out,exp)

        #Testing code input that is an infinite loop (this should cause a timeout)
        code = "while True:\n\tpass\n"
        exp = "Something went wrong running your code:\n" \
              "It took too long to execute, so we stopped it!\n"
        handler = CodeClient(host,port,code,flags)
        handler.max_time = 2
        handler.run()
        out = handler.log.replace('‘','\'').replace('’','\'')
        self.assertEqual(out,exp)

    def test_run_r(self):
        host = ''
        port = 4002
        flags = "" 

        # Testing code input with a compilation error in it
        code =  "this is bad code"
        exp =   "Rscript code.r\n" \
                "Something went wrong running your code:\n" \
                "Error: unexpected symbol in \"this is\"\n" \
                "Execution halted\n"

        handler = CodeClient(host,port,code,flags)
        handler.run()
        out = handler.compilation_log
        self.assertEqual(out,exp)

        #Testing code input that is correct (it should compile and run successfully)
        code = "hello <- \"Hello, World!\"\nprint(hello)"
        exp =   "Rscript code.r\n" \
                "Your code successfully compiled and ran, here's the output:\n" \
                "[1] \"Hello, World!\"\n"
        handler = CodeClient(host,port,code,flags)
        handler.run()
        out = handler.compilation_log
        self.assertEqual(out,exp)

        #Testing code input that is an infinite loop (this should cause a timeout)
        code = "while (TRUE)\{\}\n"
        exp = "Something went wrong running your code:\n" \
              "It took too long to execute, so we stopped it!\n"
        handler = CodeClient(host,port,code,flags)
        handler.max_time = 2
        handler.run()
        out = handler.log.replace('‘','\'').replace('’','\'')
        self.assertEqual(out,exp)

if __name__ == '__main__':
    unittest.main()
