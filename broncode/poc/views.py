from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.staticfiles import finders
from datetime import datetime


def index(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    # Get variable from template ('component/codemirror.html')
    code = request.POST.get('codearea','na')

    # Get variable from template ('component/flags.html')
    compilerFlags = request.POST.get('compilerFlags', 'na')

    # Open a file and write the contents to it
    if code != 'na':
        print(code)
        codeFile = open('testCode.c','w')
        codeFile.write(code)
        codeFile.close()
    
    # Grab sample code
    filename = finders.find('poc/samplefiles/testCode.c')
    fp = open(filename, 'r')
    sampleCode = fp.read()

    # Render the 'index.html' page
    return render(
        request,
        'poc/index.html',
        {
            'title': 'Broncode',
            'year': datetime.now().year,
            'codeText': sampleCode,
            'defaultFlags': '-g -O3'
        }
    )
