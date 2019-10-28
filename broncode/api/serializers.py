from rest_framework import serializers

from django.contrib.auth.models import User as DjangoUser
from poc.models import UserProfile
from poc.models import Course
from poc.models import Chapter
from poc.models import Lesson
from poc.models import Submission
from poc.models import SolutionSet

from poc.codeclient import CodeClient

from django.core.exceptions import ObjectDoesNotExist

class CourseSerializerLite(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title", "owners")

class LessonSerializerLite(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "title", "number")

class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoUser
        fields = ("id", "username")

class UserSerializer(serializers.ModelSerializer):
    enrolled_in = CourseSerializerLite(many=True, read_only=True)
    owned_courses = CourseSerializerLite(many=True, read_only=True)
    completed_lessons = LessonSerializerLite(many=True, read_only=True)
    user = DjangoUserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "user",
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
            "markdown",
            "example_code", 
            "compiler_flags",
            "language"
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

def extract_code_output(log, language):
    # takes the unedited output log of a program and extracts the actual program
    # output from it. this is different from the log because there are some extra
    # informational lines printed in the log such as "Executing program..." etc

    # hack: code output will be after the first x lines
    # x depends on the language (or more precisely, the docker container backend) that is used
    code_output = ""
    if language == "C":
        code_output = "\n".join(log.split('\n')[6:])
    elif language == "Python3":
        code_output = "\n".join(log.split('\n')[2:])

    return code_output

class SubmissionSerializer(serializers.ModelSerializer):
    log = serializers.CharField(read_only=True)
    passed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Submission
        fields = ("id", "user", "lesson", "code", "compiler_flags", "log", "passed")
    
    def save(self):
        """
        Run the code in docker and log it.

        How this works: in Django REST framework, data is passed to the view,
        (in this case SubmissionViewSet) which catches the data, validates it, and
        then passes it to the SubmissionSeializer (this class) to save. By overwriting
        the save method, we can inject data (the output log, and whether or not
        the code passed tests) into the model before was call the create/save function.
        """

        code = self.validated_data['code']
        flags = self.validated_data['compiler_flags']
        log = ''
        host = ''
        lesson = self.validated_data['lesson']
        if lesson.language == "C":
            port = 4000
        elif lesson.language == "Python3":
            port = 4001
        else:
            print("Unknown lesson type: {}".format(lesson.language))

        try:
            solution_set = SolutionSet.objects.get(lesson=self.validated_data['lesson'])
        except ObjectDoesNotExist:
            solution_set = None

        if solution_set:
            passed_stdin = solution_set.stdin
        else:
            passed_stdin = ""

        # handle the code execution using docker
        if code != '':
            handler = CodeClient(host,port,code,flags,passed_stdin)
            handler.run()
            log = handler.log
        else:
            log = "No code to run...\n"

        code_output = extract_code_output(log, lesson.language)

        print("code_output: ", code_output)
        print("vs: ", solution_set.stdout)

        if solution_set:
            passed_test = (code_output == solution_set.stdout)
        else:
            passed_test = True

        print("Creating submission object...")

        # you can add additional data to serializers by calling save(newdata=data)
        # so after running the code and getting the necessary data, we just call
        # the default implementation of save given to us by ModelSerializer
        return super().save(log=log, passed=passed_test)

class SolutionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionSet
        fields = ("id", "number", "lesson", "stdin", "stdout")
