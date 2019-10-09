from rest_framework import serializers

# from django.contrib.auth.models import User
from poc.models import User
from poc.models import Course
from poc.models import Chapter
from poc.models import Lesson

class CourseSerializerLite(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title")

class UserSerializer(serializers.ModelSerializer):
    enrolled_in = CourseSerializerLite(many=True, read_only=True)
    owned_courses = CourseSerializerLite(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("username","enrolled_in","owned_courses","completed_lessons")

class LessonSerializer(serializers.ModelSerializer):
    chapter = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Lesson
        fields = ("id", "title", "index", "chapter", "chapter_title", "example_code", "compiler_flags")

class LessonSerializerLite(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "title")

class ChapterSerializer(serializers.ModelSerializer):
    lessons = LessonSerializerLite(many=True, read_only=True)
    class Meta:
        model = Chapter
        fields = ("id", "title", "index", "lessons", "course_title")

class ChapterSerializerLite(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ("id", "title")

class CourseSerializer(serializers.ModelSerializer):
    owners = UserSerializer(many=True, read_only=True)
    chapters = ChapterSerializerLite(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ("id", "title", "chapters", "owners")
