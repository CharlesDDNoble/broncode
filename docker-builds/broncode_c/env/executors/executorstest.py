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
        # Testing code input that is correct (it should compile and run successfully)
        codex = CExecutor(self.good_code,self.flags)
        codex.execute()

        self.assertEqual(codex.compilation_log,self.good_exp)
        self.assertEqual(len(codex.run_logs), 0)

        os.remove("code")
        os.remove("code.c")

    def test_bad_code(self):
        # Testing code input with a compilation error in it
        codex = CExecutor(self.bad_code,self.flags)
        codex.execute()

        # GCC seems to use the curly quotes instead of regular quotes...
        codex.compilation_log = codex.compilation_log.replace('‘','\'')
        codex.compilation_log = codex.compilation_log.replace('’','\'') 
        self.assertEqual(codex.compilation_log,self.bad_exp)
        self.assertEqual(len(codex.run_logs), 0)

        os.remove("code.c")  

    def test_input(self):
        # Testing reading command line functionality
        # Program outputs argv[1] x 2

        code =  "#include <stdio.h>\n"\
                "#include <stdlib.h>\n"\
                "\n"\
                "int main(int argc, char* argv[]) {\n"\
                "    int integer;\n"\
                "    integer = atoi(argv[1]);\n"\
                "    printf(\"%d\", integer * 2);\n"\
                "    return 0;\n"\
                "}\n"

        exp  =  "gcc -o3 -o code code.c\n" \
                "Executing program...\n" \
                "Your code successfully compiled and ran, here's the output:\n" \
                "./code 2\n"
                
        exp2 =  "4"

        codex = CExecutor(code,self.flags,["2"])
        codex.execute()

        self.assertEqual(codex.compilation_log,exp)
        self.assertEqual(codex.run_logs[0], exp2)

        os.remove("code")
        os.remove("code.c")

    def test_multi_input(self):
        code =  '#include <stdio.h>\n'\
                'int main(int argc, char* argv[]) {\n'\
                '    int number;\n'\
                '    number = atoi(argv[1]);\n'\
                '    printf("%d\\n", number * 2);\n'\
                '}\n'
        flags = ""
        inputs = ["2", "4", "8"]

        comp_log =  "gcc -o code code.c\n"\
                    "Executing program...\n"\
                    "Your code successfully compiled and ran, here's the output:\n"\
                    "./code 2\n" \
                    "./code 4\n" \
                    "./code 8\n"

        codex = CExecutor(code, flags, inputs)
        codex.execute()

        self.assertEqual(codex.compilation_log, comp_log)
        self.assertEqual(len(codex.run_logs), 3)
        self.assertEqual(codex.run_logs[0], "4\n")
        self.assertEqual(codex.run_logs[1], "8\n")
        self.assertEqual(codex.run_logs[2], "16\n")

        os.remove("code")
        os.remove("code.c")

    def test_multi_word_input(self):
        code =  '#include <stdio.h>\n'\
                'int main(int argc, char* argv[]) {\n'\
                '    int number;\n'\
                '    number = atoi(argv[1]);\n'\
                '    printf("%d\\n", number * 2);\n'\
                '    number = atoi(argv[2]);\n'\
                '    printf("%d\\n", number * 2);\n'\
                '}\n'
        flags = ""
        inputs = ["2 3", "4 5", "8 9"]

        comp_log =  "gcc -o code code.c\n"\
                    "Executing program...\n"\
                    "Your code successfully compiled and ran, here's the output:\n"\
                    "./code 2 3\n" \
                    "./code 4 5\n" \
                    "./code 8 9\n"

        codex = CExecutor(code, flags, inputs)
        codex.execute()

        self.assertEqual(codex.compilation_log, comp_log)
        self.assertEqual(len(codex.run_logs), 3)
        self.assertEqual(codex.run_logs[0], "4\n6\n")
        self.assertEqual(codex.run_logs[1], "8\n10\n")
        self.assertEqual(codex.run_logs[2], "16\n18\n")

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

    def test_bad_code(self):
        code =  "bad code"
        flags = ""
        exp = "python3 code.py\n"\
              "Something went wrong running your code:\n" \
              "  File \"code.py\", line 1\n" \
              "    bad code\n" \
              "           ^\n" \
              "SyntaxError: invalid syntax\n"
        
        codex = PythonExecutor(code,flags)
        codex.execute()

        self.assertEqual(codex.compilation_log,exp)
        self.assertEqual(len(codex.run_logs), 0)

        os.remove("code.py")

    def test_input(self):
        code =  "import sys\n" \
                "print(str(int(sys.argv[1]) * 2))"
        flags = ""
        inputs = ["2"]
                
        codex = PythonExecutor(code,flags,inputs)
        codex.execute()

        self.assertEqual(codex.compilation_log,"python3 code.py 2\n")
        self.assertEqual(len(codex.run_logs), 1)
        self.assertEqual(codex.run_logs[0], "4\n")

        os.remove("code.py")

    def test_multi_input(self):
        code =  "import sys\n" \
                "print(str(int(sys.argv[1]) * 2))"
        flags = ""
        inputs = ["2", "4", "8"]
        codex = PythonExecutor(code, flags, inputs)
        codex.execute()

        self.assertEqual(codex.compilation_log, "python3 code.py 2\npython3 code.py 4\npython3 code.py 8\n")
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
    bad_code = "this is bad code"
    bad_exp = "Rscript code.r\n" \
                "Something went wrong running your code:\n" \
                "Error: unexpected symbol in \"this is\"\n" \
                "Execution halted\n"
    flags = ""

    def test_execute(self):
        # Testing code input that is correct (it should compile and run successfully)
        codex = RExecutor(self.good_code,self.flags)
        codex.execute()

        self.assertEqual(codex.compilation_log,self.good_exp)

        os.remove("code.r")

    def test_bad_code(self):
        # Testing code input with a compilation error in it
        codex = RExecutor(self.bad_code,self.flags)
        codex.execute()
        
        self.assertEqual(codex.compilation_log,self.bad_exp)
        os.remove("code.r")

    def test_input(self):
        code = "args <- commandArgs(trailingOnly=TRUE)\n" \
                "print(as.numeric(args[1]) * 2)\n"
        inputs = "2"
        codex = RExecutor(code,self.flags,inputs)
        codex.execute()
        
        self.assertEqual(len(codex.run_logs), 1)
        self.assertEqual(codex.run_logs[0], "[1] 4\n")

        os.remove("code.r")

    def test_multi_input(self):
        code = "args <- commandArgs(trailingOnly=TRUE)\n" \
                "print(as.numeric(args[1]) * 2)\n"
        inputs = ["2", "4", "8"]
        codex = RExecutor(code,self.flags,inputs)
        codex.execute()
        
        self.assertEqual(len(codex.run_logs), 3)
        self.assertEqual(codex.run_logs[0], "[1] 4\n")
        self.assertEqual(codex.run_logs[1], "[1] 8\n")
        self.assertEqual(codex.run_logs[2], "[1] 16\n")

        os.remove("code.r")

if __name__ == '__main__':
    unittest.main()
