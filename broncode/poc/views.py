from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.staticfiles import finders
from datetime import datetime
from .codehandler import CodeHandler

def index(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    # Grab sample code
    filename = finders.find('poc/samplefiles/testCode.c')
    fp = open(filename, 'r')
    sampleCode = fp.read()

    # Get variable from template ('component/codemirror.html')
    code = request.POST.get('codearea','na')

    # Get variable from template ('component/flags.html')
    compilerFlags = request.POST.get('compilerFlags', 'na')
    log = ''

    # Open a file and write the contents to it
    if code != 'na':
         handler = CodeHandler(code, 'code.c', 'broncode_c')
         log = handler.log
         sampleCode = code


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
