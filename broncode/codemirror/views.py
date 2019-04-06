from django.shortcuts import render

# Create your views here.

from django.http import Http404
from django.shortcuts import render

def index(request):
    return render(request, 'codemirror/codemirror.html')
