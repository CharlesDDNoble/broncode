import os
import random
import string
import json

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.staticfiles import finders
from datetime import datetime
from .codeclient import CodeClient
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserProfileForm
from .models import Lesson
from django.core.exceptions import ObjectDoesNotExist

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
            profile = profile.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            # Authenticate user
            user = authenticate(username=username, password=password)

            # Login
            login(request, user)
            
            # Return back
            return redirect('/')
    
    context = {'form': form, 'profile_form': profile_form}

    # Render the 'register.html' page
    return render(request, 'registration/register.html', context)

@login_required
def lesson(request, lesson_id):
    # Renders the home page.
    assert isinstance(request, HttpRequest)

    # make sure the lesson exists
    if not Lesson.objects.filter(id=lesson_id).exists():
        raise ObjectDoesNotExist

    lesson_obj = Lesson.objects.get(id=lesson_id)

    # grab lesson language
    lesson_lang = lesson_obj.language

    codemirror_lang = "text/x-csrc"

    # grab lesson text
    lesson_text = lesson_obj.markdown
    
    # grab compiler flags
    lesson_flags = lesson_obj.compiler_flags

    # grab sample code
    lesson_code = lesson_obj.example_code

    # Render the 'index.html' page
    return render(
        request,
        'poc/tutorial.html',
        {
            'title': 'Broncode',
            'year': datetime.now().year,
            'defaultFlags': '-g -O3',
            'lesson_id': lesson_id,
            'lesson_text': lesson_text,
            'lesson_flags' : lesson_flags,
            'lesson_code': lesson_code,
            'profile': request.user.userprofile,
            'codemirror_lang': codemirror_lang
        }
    )
