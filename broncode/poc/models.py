from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CODE_MAXLEN = 10000
FLAGS_MAXLEN = 512

class Course(models.Model):
    title = models.CharField(max_length=256)

class Chapter(models.Model):
    title = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Lesson(models.Model):
    title = models.CharField(max_length=128)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    example_code = models.CharField(max_length=CODE_MAXLEN, blank=True)
    compiler_flags = models.CharField(max_length=FLAGS_MAXLEN, blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128, default='')
    last_name = models.CharField(max_length=128, default='')
    email = models.EmailField(max_length=254, default='')
    enrolled_in = models.ManyToManyField(Course, blank=True)
    owned = models.ManyToManyField(Course, blank=True, related_name='owned_courses')
    completed_lessons = models.ManyToManyField(Lesson, blank=True)

    def __str__(self):
        return self.user.username

class SolutionSet(models.Model):
    ordering = models.IntegerField
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    stdin = models.CharField(max_length=2048)
    stdout = models.CharField(max_length=2048)

class Submission(models.Model):
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    code = models.CharField(max_length=CODE_MAXLEN)
    compiler_flags = models.CharField(max_length=FLAGS_MAXLEN)
    passed = models.BooleanField(default=False)
