from rest_framework import serializers
from poc.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "enrolled_in")
