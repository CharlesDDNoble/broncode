from rest_framework import serializers

# from django.contrib.auth.models import User
from poc.models import User
from poc.models import Course

class LightCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title")

class UserSerializer(serializers.ModelSerializer):
    enrolled_in = LightCourseSerializer(many=True, read_only=True)
    owned_courses = LightCourseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("username","enrolled_in","owned_courses","completed_lessons")

class CourseSerializer(serializers.ModelSerializer):
    owners = UserSerializer(many=True, read_only = False)
    class Meta:
        model = Course
        fields = ("id", "title", "chapters", "lessons", "owners")
