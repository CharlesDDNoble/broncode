from rest_framework import serializers

# from django.contrib.auth.models import User
from poc.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username","enrolled_in","owned_courses","complete_lessons")
