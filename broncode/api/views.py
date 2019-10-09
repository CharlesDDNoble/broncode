from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
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

from poc.codehandler import CodeHandler

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

class SubmissionViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def create(self, request):
        """
        Run the code in docker and log it.
        """
        
        print("Running...")

        code = request.data['code']
        flags = request.data['compiler_flags']
        log = ''
        host = ''
        port = 4000

        # handle the code execution using docker
        if code != '':
            handler = CodeHandler(host,port,code,flags)
            handler.run()
            log = handler.log
        else:
            log = "Code field was empty...\n"

        # TODO: determine if the code passed or failed tests here

        print("Creating...")

        self.get_serializer().save(log=log)

        return super().create(request)

class SolutionSetViewSet(viewsets.ModelViewSet):
    queryset = SolutionSet.objects.all()
    serializer_class = SolutionSetSerializer
