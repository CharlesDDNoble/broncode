"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    
    code = request.POST.get('codearea','na')
    if code != 'na':
        print(code)
        codeFile = open('testCode.c','w')
        codeFile.write(code)
        codeFile.close()
          
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


