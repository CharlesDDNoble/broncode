from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

#from django.contrib.auth.models import User
from poc.models import User
from .serializers import UserSerializer

from poc.models import Course
from .serializers import CourseSerializer

@api_view(['GET'])
def api_root(request):
    return Response({
        'users': reverse('user-list', request=request)
    })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
