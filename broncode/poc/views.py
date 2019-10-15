import os
import random
import string
import json

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.staticfiles import finders
from datetime import datetime
from .codehandler import CodeHandler
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserProfileForm

def index(request):
    # Renders the home page.
    assert isinstance(request, HttpRequest)
    
    # Render the 'index.html' page
    return render(request,'poc/index.html')

@login_required
def main(request):
    # Renders the home page.
    assert isinstance(request, HttpRequest)

    # Render the 'index.html' page
    return render(request,'poc/main.html')

def register(request):
    # Renders the home page.
    assert isinstance(request, HttpRequest)

    if request.method != 'POST':
        form = CustomUserCreationForm()
        profile_form = UserProfileForm()
    else:
        form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            
            profile.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            # Authenticate user
            user = authenticate(username=username, password=password)

            # Login
            login(request, user)
            
            # Return back
            return redirect('/poc')
    
    context = {'form': form, 'profile_form': profile_form}

    # Render the 'index.html' page
    return render(request, 'registration/register.html', context)

def lesson(request, lesson_id):
    # Renders the home page.
    assert isinstance(request, HttpRequest)
    
    # Grab sample code
    filename = finders.find('poc/samplefiles/testCode.c')
    fp = open(filename, 'r')
    sampleCode = fp.read()

    # Render the 'index.html' page
    return render(
        request,
        'poc/tutorial.html',
        {
            'title': 'Broncode',
            'year': datetime.now().year,
            'codeText': sampleCode,
            'defaultFlags': '-g -O3',
            'lesson_id': lesson_id
        }
    )
