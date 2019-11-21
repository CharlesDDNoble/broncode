import os
import random
import string
import json

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.staticfiles import finders
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .forms import CustomUserCreationForm, UserProfileForm
from .models import Lesson, Course
from .codeclient import CodeClient


def index(request):
    assert isinstance(request, HttpRequest)
    
    if request.user.is_authenticated:
        return redirect('/course/')

    # Render the 'index.html' page
    return render(request,'poc/index.html')

def register(request):
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
def lesson(request, course_id, lesson_number):
    assert isinstance(request, HttpRequest)
    
    # make sure the lesson exists
    if not Lesson.objects.filter(course=course_id, number=lesson_number).exists():
        raise ObjectDoesNotExist
    
    
    lesson_obj = Lesson.objects.filter(course=course_id, number=lesson_number)[0]

    disable_codemirror_1 = ''
    disable_codemirror_2 = ''
    disable_codemirror = request.GET.get("disableCodemirror","False")

    if not disable_codemirror == "False":
        disable_codemirror_1 = '<!--'
        disable_codemirror_2 = '-->'

    # grab lesson language
    lesson_lang = lesson_obj.language

    codemirror_lang_name = "text/x-csrc"
    codemirror_lang_args = ""
    if lesson_lang == "Python3":
        codemirror_lang_name = "python"
        codemirror_lang_args = ", version: 3, singleLineStringErrors: false"

    print("lesson_obj=---===============",lesson_obj)
    print(lesson_obj.id)

    # grab lesson text
    lesson_text = lesson_obj.markdown
    
    # grab compiler flags
    lesson_flags = lesson_obj.compiler_flags

    # grab sample code
    lesson_code = lesson_obj.example_code

    # initialize context
    context = {
            'title': 'Broncode',
            'year': datetime.now().year,
            'defaultFlags': '-g -O3',
            'lesson_id': lesson_obj.id,
            'lesson_text': lesson_text,
            'lesson_flags' : lesson_flags,
            'lesson_code': lesson_code,
            'profile': request.user.userprofile,
            'codemirror_lang_name': codemirror_lang_name,
            'codemirror_lang_args': codemirror_lang_args,
            'disable_codemirror_1': disable_codemirror_1,
            'disable_codemirror_2': disable_codemirror_2
        }

    # Render the 'index.html' page
    return render(request, 'poc/lesson.html', context)

@login_required
def course(request):
    # Renders the home page.
    assert isinstance(request, HttpRequest)

    # Initialize context
    context = {'courses': Course.objects.all() }

    # Render the 'index.html' page
    return render(request,'poc/course.html', context)

@login_required
def lessonList(request, course_id):
    assert isinstance(request, HttpRequest)
    
    # Initialize context
    context = {
        'lessons': Lesson.objects.filter(course=course_id).order_by('number'),
        'course_id': course_id,
    }

    return render(request, 'poc/lesson-list.html', context)

@login_required
def createLesson(request, course_id):
    assert isinstance(request, HttpRequest)
    print("COURSE_ID:", course_id)

    lesson_numbers = Lesson.objects.filter(course=course_id).values_list('number', flat=True).order_by('-number')
    print("Lesson_numbers:", lesson_numbers)

    if len(lesson_numbers) == 0:
        new_lesson_number = 1
    else:
        new_lesson_number = lesson_numbers[0] + 1
    

    # Initialize context
    context = {'course_id': course_id, 'new_lesson_number': new_lesson_number}

    return render(request, 'poc/create-lesson.html', context)