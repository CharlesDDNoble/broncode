from rest_framework import serializers
from poc.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("username", "password", "enrolled_in")
