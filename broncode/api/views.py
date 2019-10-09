from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from django.contrib.auth.models import User
from .serializers import UserSerializer

@api_view(['GET'])
def api_root(request):
    return Response({
        'users': reverse('user-list', request=request)
    })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
