from rest_framework import generics
from poc.models import User
from .serializers import UserSerializer

class ListUsersView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
