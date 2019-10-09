from rest_framework import serializers

from django.contrib.auth.models import User
from poc.models import Course

class CourseSerializer(serializers.ModelSerializer):
    # owners = UserSerializer(many=True)
    class Meta:
        model = Course
        fields = ("title", "owners")

class UserSerializer(serializers.ModelSerializer):
    owned_courses = CourseSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ("username","email","owned_courses")

