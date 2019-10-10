from rest_framework import serializers

# from django.contrib.auth.models import User
from poc.models import User
from poc.models import Course
from poc.models import Chapter
from poc.models import Lesson
from poc.models import Submission
from poc.models import SolutionSet

from poc.codehandler import CodeHandler

class CourseSerializerLite(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title", "owners")

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
        fields = (
            "username", 
            "enrolled_in", 
            "owned_courses", 
            "completed_lessons", 
            "submissions"
        )

class ChapterSerializerLite(serializers.ModelSerializer):
    course = CourseSerializerLite(read_only=True)
    class Meta:
        model = Chapter
        fields = ("id", "title", "number", "course")

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "id", 
            "title", 
            "number", 
            "chapter",
            "example_code", 
            "compiler_flags"
        )

class ChapterSerializer(serializers.ModelSerializer):
    lessons = LessonSerializerLite(many=True, read_only=True)
    class Meta:
        model = Chapter
        fields = ("id", "title", "number", "lessons", "course")

class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializerLite(many=True, read_only=True)
    owners = UserSerializer(many=True, read_only=True)
    enrolled_users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ("id", "title", "chapters", "owners", "enrolled_users")

class SubmissionSerializer(serializers.ModelSerializer):
    log = serializers.CharField(read_only=True)
    passed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Submission
        fields = ("id", "username", "lesson", "code", "compiler_flags", "log", "passed")
    
    def save(self):
        """
        Run the code in docker and log it.

        How this works: in Django REST framework, data is passed to the view,
        (in this case SubmissionViewSet) which catches the data, validates it, and
        then passes it to the SubmissionSeializer (this class) to save. By overwriting
        the save method, we can inject data (the output log, and whether or not
        the code passed tests) into the model before was call the create/save function.
        """
        print("Running code...")

        code = self.validated_data['code']
        flags = self.validated_data['compiler_flags']
        log = ''
        host = ''
        port = 4000

        # handle the code execution using docker
        if code != '':
            handler = CodeHandler(host,port,code,flags)
            handler.run()
            log = handler.log
        else:
            log = "No code to run...\n"

        # TODO: determine if the code passed or failed tests here

        print("Creating submission object...")

        # you can add additional data to serializers by calling save(newdata=data)
        # so after running the code and getting the necessary data, we just call
        # the default implementation of save given to us by ModelSerializer
        return super().save(log=log)

class SolutionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionSet
        fields = ("id", "number", "lesson", "stdin", "stdout")
