from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.staticfiles import finders
from datetime import datetime
from .codehandler import CodeHandler
import os
import random
import string
from django.http import HttpResponse
import json

def index(request):
    # Renders the home page.
    assert isinstance(request, HttpRequest)
    
    # Render the 'index.html' page
    return render(
        request,
        'poc/index.html',
        {
            'title': 'Broncode',
            'year': datetime.now().year,
        }
    )

def main(request):
    # Renders the home page.
    assert isinstance(request, HttpRequest)

    # Render the 'index.html' page
    return render(
        request,
        'poc/main.html',
        {
            'title': 'Broncode',
            'year': datetime.now().year,
        }
    )


def tutorial(request):
    # Renders the home page.
    assert isinstance(request, HttpRequest)
    
    # Grab sample code
    filename = finders.find('poc/samplefiles/testCode.c')
    fp = open(filename, 'r')
    sampleCode = fp.read()


    if request.method == 'POST':
        print(request.POST)
        code = request.POST.get('codearea','na')
        compilerFlags = request.POST.get('compileFlags', 'na')
        log = ''
        host = ''
        port = 4000

        # handle the code execution using docker
        if code != 'na':
            handler = CodeHandler(host,port,code,compilerFlags)
            handler.run()
            log = handler.log
        else:
            print("dammit")
        return HttpResponse(
            content=json.dumps(log),
            content_type="application/json"
        )
    else:
        

        # # Get variable from template ('component/codemirror.html')
        # code = request.POST.get('codearea','na')

        # # Get variable from template ('component/flags.html')
        # compilerFlags = request.POST.get('compileFlags', 'na')
        # log = ''
        # host = ''
        # port = 4000
        # # handle the code execution using docker
        # if code != 'na':
        #     handler = CodeHandler(host,port,code,compilerFlags)
        #     handler.run()
        #     log = handler.log
        #     sampleCode = code
    
        # Render the 'index.html' page
        return render(
            request,
            'poc/tutorial.html',
            {
                'title': 'Broncode',
                # 'year': datetime.now().year,
                # 'codeText': sampleCode,
                # 'defaultFlags': '-g -O3'
            }
        )
