import unittest
import os
from .cexecutor import CExecutor
from .pythonexecutor import PythonExecutor

class CExecutorTest(unittest.TestCase):
    flags = "-o3"
    bad_code =  "int main(int argc,char** argv){error;return 0;}\n"
    bad_exp  =  "Parsing gcc flags...\n" \
                "Compiling code...\n" \
                "gcc -o3 -o code code.c\n" \
                "Something went wrong compiling your code:\n" \
                "code.c: In function 'main':\n" \
                "code.c:1:32: error: 'error' undeclared (first use in this function)\n" \
                " int main(int argc,char** argv){error;return 0;}\n" \
                "                                ^~~~~\n" \
                "code.c:1:32: note: each undeclared identifier is reported only once for each function it appears in\n"

    good_code = "int main(int argc,char** argv){printf(\"Hello!\\n\");return 0;}\n"
    good_exp  = "Parsing gcc flags...\n" \
                "Compiling code...\n" \
                "gcc -o3 -o code code.c\n" \
                "Executing program...\n" \
                "./code\n" \
                "Your code successfully compiled and ran, here's the output:\n" \
                "Hello!\n"
    # inf_code = "int main(int argc,char** argv){while(1);return 0;}\n"

    def test_compile_and_run(self):
        # Testing code input with a compilation error in it
        codex = CExecutor(self.bad_code,self.flags)
        done_process = codex.compile()
        out = done_process.stderr.decode("utf-8")
        exp = self.bad_exp[104:]
        # GCC seems to use the curly quotes ‘’ instead of regular quote ''
        out = out.replace('‘','\'')
        out = out.replace('’','\'')
        self.assertNotEqual(done_process.returncode,0)
        self.assertEqual(out,exp)
        
        # Testing code input that is correct (it should compile and run successfully)
        codex = CExecutor(self.good_code,self.flags)
        
        done_process = codex.compile()
        self.assertEqual(done_process.returncode,0)
        
        done_process = codex.run()
        out = done_process.stdout.decode("utf-8")
        exp = "Hello!\n"
        self.assertEqual(done_process.returncode,0)
        self.assertEqual(out,exp)

        os.remove("code")
        os.remove("code.c")

    def test_execute(self):
        # Testing code input with a compilation error in it
        codex = CExecutor(self.bad_code,self.flags)
        codex.execute()

        # GCC seems to use the curly quotes instead of regular quotes...
        codex.log = codex.log.replace('‘','\'')
        codex.log = codex.log.replace('’','\'') 
        self.assertEqual(codex.log,self.bad_exp)

        # Testing code input that is correct (it should compile and run successfully)
        codex = CExecutor(self.good_code,self.flags)
        codex.execute()

        self.assertEqual(codex.log,self.good_exp)

        os.remove("code")
        os.remove("code.c")

class PythonExecutorTest(unittest.TestCase):

    good_code = "print(\"Hello World!\")"
    good_exp =  "python3 code.py\n" \
                "Your code successfully compiled and ran, here's the output:\n" \
                "Hello World!\n"
    bad_code = "print(Erro World!)"
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
        
        self.assertEqual(codex.log,self.bad_exp)

        # Testing code input that is correct (it should compile and run successfully)
        codex = PythonExecutor(self.good_code,self.flags)
        codex.execute()

        self.assertEqual(codex.log,self.good_exp)

        os.remove("code.py")


if __name__ == '__main__':
    unittest.main()