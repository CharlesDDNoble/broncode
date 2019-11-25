from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=128)
    number = models.IntegerField()
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    markdown = models.TextField()
    example_code = models.TextField()
    compiler_flags = models.TextField(blank=True)
    language = models.CharField(max_length=16)

    class Meta:
        unique_together = ['course', 'number']
    
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128, default='')
    last_name = models.CharField(max_length=128, default='')
    email = models.EmailField(max_length=254, default='')
    enrolled_in = models.ManyToManyField(Course, blank=True)
    owned_courses = models.ManyToManyField(Course, blank=True, related_name='owners')
    completed_lessons = models.ManyToManyField(Lesson, blank=True)

    def __str__(self):
        return self.user.username

class SolutionSet(models.Model):
    # number:
    # order that the tests will be run in.
    # this is here to enable the capability to say "you passed/failed test number 1"
    # and have it always refer to the same test
    number = models.IntegerField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="solution_sets")
    stdin = models.TextField(default="", blank=True)
    stdout = models.TextField()
    hint = models.TextField(default="", blank=True)

    class Meta:
        unique_together = ['lesson', 'number']

class Submission(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="submissions")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="submissions")
    code = models.TextField(blank=False)
    compiler_flags = models.TextField(blank=True)
    user_tested = models.BooleanField() # if true, this submission has stdin provided by the user
    stdin = models.TextField(blank=True)
    passed = models.BooleanField(default=False)
    log = models.TextField(blank=True)
