from django.http import HttpResponse

from rest_framework import generics
from poc.models import UserProfile
from .serializers import UserSerializer

def index(request):
    return HttpResponse("Welcome to the broncode api :)")

class ListUsersView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

