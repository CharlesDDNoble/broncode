from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

#from django.contrib.auth.models import User
from poc.models import User
from .serializers import UserSerializer

from poc.models import Course
from .serializers import CourseSerializer

from poc.models import Chapter
from .serializers import ChapterSerializer

from poc.models import Lesson
from .serializers import LessonSerializer

from poc.models import Submission
from .serializers import SubmissionSerializer

from poc.models import SolutionSet
from .serializers import SolutionSetSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class SolutionSetViewSet(viewsets.ModelViewSet):
    queryset = SolutionSet.objects.all()
    serializer_class = SolutionSetSerializer