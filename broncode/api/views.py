from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import api_view

from django.contrib.auth.models import User
from .serializers import UserSerializer

@api_view(['GET'])
def api_root(request):
    return Response({
        'users': reverse('user-list', request=request)
    })

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
