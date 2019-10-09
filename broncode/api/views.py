from django.http import HttpResponse

from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer

def index(request):
    return HttpResponse("Welcome to the broncode api :)")

class UserViewSet(viewsets.ModelViewSet):
    """
    Provides a get method handler.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
