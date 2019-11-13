from rest_framework import serializers

from django.contrib.auth.models import User as DjangoUser
from poc.models import UserProfile
from poc.models import Course
# from poc.models import Chapter
from poc.models import Lesson
from poc.models import Submission
from poc.models import SolutionSet

from poc.codeclient import CodeClient

from django.core.exceptions import ObjectDoesNotExist

import random

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

# class ChapterSerializerLite(serializers.ModelSerializer):
#     course = CourseSerializerLite(read_only=True)
#     class Meta:
#         model = Chapter
#         fields = ("id", "title", "number", "course")

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "id", 
            "title", 
            "number", 
            "course",
            "markdown",
            "example_code", 
            "compiler_flags",
            "language"
        )

# class ChapterSerializer(serializers.ModelSerializer):
#     lessons = LessonSerializerLite(many=True, read_only=True)
#     class Meta:
#         model = Chapter
#         fields = ("id", "title", "number", "lessons", "course")

class CourseSerializer(serializers.ModelSerializer):
    # chapters = ChapterSerializerLite(many=True, read_only=True)
    lessons = LessonSerializerLite(many=True, read_only=True)
    owners = UserSerializer(many=True, read_only=True)
    enrolled_users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        # Changed `chapters` to `lessons`
        fields = ("id", "title", "lessons", "owners", "enrolled_users")

class SubmissionSerializer(serializers.ModelSerializer):
    log = serializers.CharField(read_only=True)
    passed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Submission
        fields = ("id", "user", "lesson", "code", "compiler_flags", "user_tested", "stdin", "log", "passed")
    
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
        user_tested = self.validated_data['user_tested']
        if lesson.language == "C":
            port = 4000
        elif lesson.language == "Python3":
            port = 4001
        elif lesson.language == "R":
            port = 4002
        else:
            print("Unknown lesson type: {}".format(lesson.language))
            raise "Unkown lesson type"

        if not user_tested:
            solution_sets = SolutionSet.objects.filter(lesson=self.validated_data['lesson'])

            if len(solution_sets) == 0:
                solution_sets = []
        else:
            solution_sets = []

        inputs = []
        if not user_tested:
            for sset in solution_sets:
                inputs.append(sset.stdin)
        else:
            inputs.append(self.validated_data['stdin'])

        # handle the code execution using docker
        if code != '':
            handler = CodeClient(host,port,code,flags,inputs)
            handler.run()
            log = handler.log
        else:
            log = "No code to run...\n"

        passed_test = False

        tests_failed = []
        if user_tested:
            passed_test = False
        elif inputs:
            passed_test = True
            for i in range(len(solution_sets)):
                print(handler.run_logs[i].rstrip() + " vs " + solution_sets[i].stdout)
                if handler.run_logs[i].rstrip() != solution_sets[i].stdout:
                    tests_failed.append(str(solution_sets[i].number))
                    passed_test = False
        else:
            passed_test = True

        if not user_tested:
            if passed_test:
                log = "You passed all tests!"
            else:
                log = "You didn't pass every test. You failed:\n"
                if len(tests_failed) == 1:
                    log += "Test {}.".format(tests_failed[0])
                else:
                    log += "Tests "
                    for i in range(len(tests_failed) - 1):
                        log += tests_failed[i] + ", "
                    log += "and {}.".format(tests_failed[-1])

        # you can add additional data to serializers by calling save(newdata=data)
        # so after running the code and getting the necessary data, we just call
        # the default implementation of save given to us by ModelSerializer
        return super().save(log=log, passed=passed_test)

class SolutionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionSet
        fields = ("id", "number", "lesson", "stdin", "stdout")
