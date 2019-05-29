#!/usr/bin/python3.6
from codehandler import CodeHandler


def test_handler(code,flags,name,image,test_string):
	print(test_string)
	handler = CodeHandler(code, flags, name, image)
	handler.run()
	print(handler.log)

def main():	
	#Test working code
	code = '#include <stdio.h>\nint main(){printf(\"Hello World!\\n\");}'
	flags = ''
	name = 'code.c'
	image = 'broncode_c'
	test_string = 'Working Hello World Example!'

	test_handler(code,flags,name,image,test_string)

	#Test error code
	code = '#include <stdio.h>\nerror'
	flags = ''
	name = 'code.c'
	image = 'broncode_c'
	test_string = 'Working Hello World Example!'

	test_handler(code,flags,name,image,test_string)

	#Test infinite loop - timeout
	code = '#include <stdio.h>\nint main(){for(;;);}'
	flags = ''
	name = 'code.c'
	image = 'broncode_c'
	test_string = 'Testing an infinite loop Example!'

	test_handler(code,flags,name,image,test_string)

	#Test a long loop
	code = '#include <stdio.h>\nint main(){int x=0;while(x < 0xFFFF) printf(\"x = %d\\n\",x++);}'
	flags = ''
	name = 'code.c'
	image = 'broncode_c'
	test_string = 'Testing long loop!'

	test_handler(code,flags,name,image,test_string)

	#Test flags using Wall and Werror 
	code = '#include <stdio.h>\nint main(){int error;printf(\"Hello World!\\n\");}'
	flags = '-Wall -Werror'
	name = 'code.c'
	image = 'broncode_c'
	test_string = 'Testing passing flags using Werror Example!'

	test_handler(code,flags,name,image,test_string)

if __name__ == "__main__":
	main()
