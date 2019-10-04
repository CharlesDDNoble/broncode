import random
import string
import json

from django.shortcuts import render, redirect
from django.contrib.staticfiles import finders
from django.http import HttpRequest
from datetime import datetime
from .codehandler import CodeHandler
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from poc.CustomUserCreationForm import CustomUserCreationForm

def index(request):
    # Renders the home page.
    assert isinstance(request, HttpRequest)
    
    # Render the 'index.html' page
    return render(request, 'poc/index.html')

def main(request):
    # Renders the home page.
    assert isinstance(request, HttpRequest)

    # Render the 'index.html' page
    return render(request, 'poc/main.html')

def register(request):
    # Renders the home page.
    assert isinstance(request, HttpRequest)

    if request.method != 'POST':
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            # Authenticate user
            user = authenticate(username=username, password=password)

            # Login
            login(request, user)
            
            # Return back
            return redirect('/poc')
    
    context = {'form': form}

    # Render the 'index.html' page
    return render(request, 'registration/register.html', context)

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
        else :
            print("dammit")
        return HttpResponse(
            content=json.dumps(log),
            content_type="application/json"
        )
    else:
        

        # Get variable from template ('component/codemirror.html')
        code = request.POST.get('codearea','na')

        # Get variable from template ('component/flags.html')
        compilerFlags = request.POST.get('compileFlags', 'na')
        log = ''
        host = ''
        port = 4000
        # handle the code execution using docker
        if code != 'na':
            handler = CodeHandler(host,port,code,compilerFlags)
            handler.run()
            log = handler.log
            sampleCode = code
    
        # Render the 'index.html' page
        return render(
            request,
            'poc/tutorial.html',
            {
                'title': 'Broncode',
                'year': datetime.now().year,
                'codeText': sampleCode,
                'defaultFlags': '-g -O3',
                'testResult' : log
            }
        )
