from codehandler import CodeHandler

code = "print(\"This is the iris dataset in R\\n\")\nhead(iris)"
file_name = 'code.r'
image_name = 'broncode_r'

handler = CodeHandler(code, file_name, image_name)
print(handler.log)


code = "import string\nfor i in range(0,26):\n\tprint(string.ascii_lowercase[:i])"
file_name = 'code.py'
image_name = 'broncode_python'

handler = CodeHandler(code, file_name, image_name)
print(handler.log)


#code = "main(c){putchar(c+'@');c^'?'^'%'?main(++c):c;}"
code = "#include <stdio.h>\n#include <limits.h>\nint main(){int c=SHRT_MAX/4;\nwhile(c--){putchar(c%2?47:92);}return c;}"
file_name = 'code.c'
image_name = 'broncode_c'

handler = CodeHandler(code, file_name, image_name)
print(handler.log)
