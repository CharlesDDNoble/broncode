from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.staticfiles import finders
from datetime import datetime
from .codehandler import CodeHandler
import os
import random
import string

def index(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    # Grab sample code
    filename = finders.find('poc/samplefiles/testCode.c')
    fp = open(filename, 'r')
    sampleCode = fp.read()

    # Get variable from template ('component/codemirror.html')
    code = request.POST.get('codearea','na')

	# Current solution to handling concurrent requests:
	# generate a random string to use as a directory name for file IO
	# NOTE: this can later be replaced with a unique identifer (user id)
    alpha_num = string.ascii_letters + string.digits
    name = ''.join(random.choices(alpha_num, k = 32))
    os.mkdir(name)
	os.chdir(name)	

    # Get variable from template ('component/flags.html')
    compilerFlags = request.POST.get('compileFlags', 'na')
    log = ''

    # Open a file and write the contents to it
    if code != 'na':
         handler = CodeHandler(code, compilerFlags, 'code.c', 'broncode_c')
         handler.run()
         log = handler.log
         sampleCode = code

	#clean-up temporary directory	
	os.chdir("..")	
	os.rmdir(name)
	

    # Render the 'index.html' page
    return render(
        request,
        'poc/index.html',
        {
            'title': 'Broncode',
            'year': datetime.now().year,
            'codeText': sampleCode,
            'defaultFlags': '-g -O3',
            'testResult' : log
        }
    )
