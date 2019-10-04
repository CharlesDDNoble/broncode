from rest_framework import serializers
#from poc.models import User
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username","email")

