from django.db import models

# Create your models here.

CODE_MAXLEN = 4096
FLAGS_MAXLEN = 512

class Course(models.Model):
    title = models.CharField(max_length=256)

class Chapter(models.Model):
    title = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Lesson(models.Model):
    title = models.CharField(max_length=128)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    example_code = models.CharField(max_length=CODE_MAXLEN)
    compiler_flags = models.CharField(max_length=FLAGS_MAXLEN)

class User(models.Model):
    username = models.CharField(max_length=64, primary_key=True)
    password = models.CharField(max_length=128)
    enrolled_in = models.ManyToManyField(Course)
    owned = models.ManyToManyField(Course, related_name='owned_courses')
    completed_lessons = models.ManyToManyField(Lesson)

class SolutionSet(models.Model):
    ordering = models.IntegerField
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    stdin = models.CharField(max_length=2048)
    stdout = models.CharField(max_length=2048)

class Submission(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    code = models.CharField(max_length=CODE_MAXLEN)
    compiler_flags = models.CharField(max_length=FLAGS_MAXLEN)
    passed = models.BooleanField(default=False)
