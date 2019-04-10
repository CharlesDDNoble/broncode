from codehandler import CodeHandler
from cexecutor import CExecutor
from pythonexecutor import PythonExecutor
from rexecutor import RExecutor
'''
code = '#include <stdio.h>\nvoid main(void*){printf(\"Blast off!\\n\");}'
file_name = 'code.c'
image_name = 'broncode_c'
code_hand = CodeHandler(code,file_name,image_name)
'''

codex = CExecutor()
codex.execute()
print(codex.log)

codex = PythonExecutor()
codex.execute()
print(codex.log)

codex = RExecutor()
codex.execute()
print(codex.log)