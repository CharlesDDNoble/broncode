from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission, SAFE_METHODS

#from django.contrib.auth.models import User
from poc.models import UserProfile
from .serializers import UserSerializer

from poc.models import Course
from .serializers import CourseSerializer

from poc.models import Lesson
from .serializers import LessonSerializer

from poc.models import Submission
from .serializers import SubmissionSerializer

from poc.models import SolutionSet
from .serializers import SolutionSetSerializer

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    lookup_field = "user"

class LessonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser|ReadOnly]

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser|ReadOnly]

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action == "create":
            perms = [IsAuthenticated]
        else:
            perms = [IsAdminUser]
        return [perm() for perm in perms]
    
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class SolutionSetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = SolutionSet.objects.all()
    serializer_class = SolutionSetSerializer
