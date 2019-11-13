import unittest
import os
from .cexecutor import CExecutor
from .pythonexecutor import PythonExecutor
from .rexecutor import RExecutor

class CExecutorTest(unittest.TestCase):
    flags = "-o3"
    bad_code =  "int main(int argc,char** argv){error;return 0;}\n"
    bad_exp  =  "gcc -o3 -o code code.c\n" \
                "Something went wrong compiling your code:\n" \
                "code.c: In function 'main':\n" \
                "code.c:1:32: error: 'error' undeclared (first use in this function)\n" \
                " int main(int argc,char** argv){error;return 0;}\n" \
                "                                ^~~~~\n" \
                "code.c:1:32: note: each undeclared identifier is reported only once for each function it appears in\n"

    good_code = "int main(int argc,char** argv){printf(\"Hello!\\n\");return 0;}\n"
    good_exp  = "gcc -o3 -o code code.c\n" \
                "Executing program...\n" \
                "Your code successfully compiled and ran, here's the output:\n" \
                "./code\n" \
                "Hello!\n"
    inf_code = "int main(int argc,char** argv){while(1);return 0;}\n"

    def test_compile_and_run(self):
        # Testing code input with a compilation error in it
        exp = "code.c: In function 'main':\n"\
              "code.c:1:32: error: 'error' undeclared (first use in this function)\n"\
              " int main(int argc,char** argv){error;return 0;}\n"\
              "                                ^~~~~\n"\
              "code.c:1:32: note: each undeclared identifier is reported only once for each function it appears in\n"\

        codex = CExecutor(self.bad_code,self.flags)
        done_process = codex.compile()
        out = done_process.stderr.decode("utf-8")
        # GCC seems to use the curly quotes ‘’ instead of regular quote ''
        out = out.replace('‘','\'')
        out = out.replace('’','\'')
        self.assertNotEqual(done_process.returncode,0)
        self.assertEqual(out,exp)
        
        # Testing code input that is correct (it should compile and run successfully)
        codex = CExecutor(self.good_code,self.flags)
        
        done_process = codex.compile()
        self.assertEqual(done_process.returncode,0)
        
        codex.run()
        out = codex.compilation_log
        exp =   "gcc -o3 -o code code.c\n"\
                "Your code successfully compiled and ran, here's the output:\n"\
                "./code\n"\
                "Hello!\n"
        self.assertEqual(done_process.returncode,0)
        self.assertEqual(out,exp)

        os.remove("code")
        os.remove("code.c")

    def test_execute(self):
        # Testing code input with a compilation error in it
        codex = CExecutor(self.bad_code,self.flags)
        codex.execute()

        # GCC seems to use the curly quotes instead of regular quotes...
        codex.compilation_log = codex.compilation_log.replace('‘','\'')
        codex.compilation_log = codex.compilation_log.replace('’','\'') 
        self.assertEqual(codex.compilation_log,self.bad_exp)

        # Testing code input that is correct (it should compile and run successfully)
        codex = CExecutor(self.good_code,self.flags)
        codex.execute()

        self.assertEqual(codex.compilation_log,self.good_exp)

        os.remove("code")
        os.remove("code.c")

    def test_stdin(self):
        # Testing reading stdin functionality
        # Program outputs stdin x 2

        code =  "#include <stdio.h>\n"\
                "#include <stdlib.h>\n"\
                "\n"\
                "int main() {\n"\
                "    int integer;\n"\
                "    int r;\n"\
                "    long unsigned int size = 128;\n"\
                "    char *buf;\n"\
                "    buf = malloc(128*sizeof(char));\n"\
                "    r = getline(&buf, &size, stdin);\n"\
                "    integer = atoi(buf);\n"\
                "    printf(\"%d\", integer * 2);\n"\
                "    return 0;\n"\
                "}\n"

        exp  =  "gcc -o3 -o code code.c\n" \
                "Executing program...\n" \
                "Your code successfully compiled and ran, here's the output:\n" \
                "./code\n"
                
        exp2 =  "4\n"

        codex = CExecutor(code,self.flags,["2"])
        codex.execute()

        self.assertEqual(codex.compilation_log,exp)
        self.assertEqual(codex.run_logs[0], exp2)

        os.remove("code")
        os.remove("code.c")

    def test_multi_input(self):
        code =  '#include <stdio.h>\n'\
                'int main() {\n'\
                '    int number;\n'\
                '    scanf("%d", &number);\n'\
                '    printf("%d\\n", number * 2);\n'\
                '}\n'
        flags = ""
        inputs = ["2", "4", "8"]

        comp_log =  "gcc -o code code.c\n"\
                    "Executing program...\n"\
                    "Your code successfully compiled and ran, here's the output:\n"\
                    "./code\n"

        codex = CExecutor(code, flags, inputs)
        codex.execute()

        self.assertEqual(codex.compilation_log, comp_log)
        self.assertEqual(len(codex.run_logs), 3)
        self.assertEqual(codex.run_logs[0], "4\n")
        self.assertEqual(codex.run_logs[1], "8\n")
        self.assertEqual(codex.run_logs[2], "16\n")

        os.remove("code")
        os.remove("code.c")       

class PythonExecutorTest(unittest.TestCase):

    good_code = "print(\"Hello World!\")"
    good_exp =  "python3 code.py\n" \
                "Your code successfully compiled and ran, here's the output:\n" \
                "Hello World!\n"
    bad_code =  "print(Erro World!)"
    bad_exp =   "python3 code.py\n" \
                "Something went wrong running your code:\n" \
                "  File \"code.py\", line 1\n" \
                "    print(Erro World!)\n" \
                "                   ^\n" \
                "SyntaxError: invalid syntax\n"
    flags = ""

    def test_execute(self):
        # Testing code input with a compilation error in it
        codex = PythonExecutor(self.bad_code,self.flags)
        codex.execute()
        
        self.assertEqual(codex.compilation_log,self.bad_exp)

        # Testing code input that is correct (it should compile and run successfully)
        codex = PythonExecutor(self.good_code,self.flags)
        codex.execute()

        self.assertEqual(codex.compilation_log,self.good_exp)

        os.remove("code.py")

    def test_multi_input(self):
        code = "print(str(int(input()) * 2))"
        flags = ""
        inputs = ["2", "4", "8"]
        codex = PythonExecutor(code, flags, inputs)
        codex.execute()

        self.assertEqual(codex.compilation_log, "python3 code.py\n")
        self.assertEqual(len(codex.run_logs), 3)
        self.assertEqual(codex.run_logs[0], "4\n")
        self.assertEqual(codex.run_logs[1], "8\n")
        self.assertEqual(codex.run_logs[2], "16\n")

        os.remove("code.py")

class RExecutorTest(unittest.TestCase):

    good_code = "hello <- \"Hello, World!\"\nprint(hello)"
    good_exp =  "Rscript code.r\n" \
                "Your code successfully compiled and ran, here's the output:\n" \
                "[1] \"Hello, World!\"\n"
#    bad_code = "print(Erro World!)"
#    bad_exp =   "python3 code.py\n" \
#                "Something went wrong running your code:\n" \
#                "  File \"code.py\", line 1\n" \
#                "    print(Erro World!)\n" \
#                "                   ^\n" \
#                "SyntaxError: invalid syntax\n"
    flags = ""

    def test_execute(self):
        # Testing code input with a compilation error in it
        #codex = RExecutor(self.bad_code,self.flags)
        #codex.execute()
        
        #self.assertEqual(codex.log,self.bad_exp)

        # Testing code input that is correct (it should compile and run successfully)
        codex = RExecutor(self.good_code,self.flags)
        codex.execute()

        self.assertEqual(codex.compilation_log,self.good_exp)

        os.remove("code.r")

if __name__ == '__main__':
    unittest.main()
