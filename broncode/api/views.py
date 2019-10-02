from Django import HttpResponse

from rest_framework import generics
from poc.models import User
from .serializers import UserSerializer

def index(request):
    return HttpResponse("Welcome to the broncode api :)")

class ListUsersView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
