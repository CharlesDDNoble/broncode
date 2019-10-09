from rest_framework import serializers

# from django.contrib.auth.models import User
from poc.models import User
from poc.models import Course
from poc.models import Chapter
from poc.models import Lesson
from poc.models import Submission

class CourseSerializerLite(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title")

class LessonSerializerLite(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "title", "number")

class UserSerializer(serializers.ModelSerializer):
    enrolled_in = CourseSerializerLite(many=True, read_only=True)
    owned_courses = CourseSerializerLite(many=True, read_only=True)
    completed_lessons = LessonSerializerLite(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("username", "enrolled_in", "owned_courses", "completed_lessons", "submissions")

class ChapterSerializerLite(serializers.ModelSerializer):
    course = CourseSerializerLite(read_only=True)
    class Meta:
        model = Chapter
        fields = ("id", "title", "number", "course")

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ("username", "lesson", "code", "compiler_flags", "passed")

class LessonSerializer(serializers.ModelSerializer):
    chapter_info = ChapterSerializerLite(read_only=True)
    submissions = SubmissionSerializer(read_only=True)
    class Meta:
        model = Lesson
        fields = (
            "id", 
            "title", 
            "number", 
            "chapter", 
            "chapter_info", 
            "example_code", 
            "compiler_flags", 
            "submissions"
        )

class ChapterSerializer(serializers.ModelSerializer):
    lessons = LessonSerializerLite(many=True, read_only=True)
    course = CourseSerializerLite(read_only=True)
    class Meta:
        model = Chapter
        fields = ("id", "title", "number", "lessons", "course")

class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializerLite(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ("id", "title", "chapters", "owners", "enrolled_users")

