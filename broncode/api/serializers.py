from rest_framework import serializers

# from django.contrib.auth.models import User
from poc.models import User
from poc.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id, title")

class UserSerializer(serializers.ModelSerializer):
    enrolled_in = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("username","enrolled_in","owned_courses","completed_lessons")
