from django.db import models

# Create your models here.

FLAGS_MAXLEN = 512

class Course(models.Model):
    title = models.CharField(max_length=256)

class Chapter(models.Model):
    title = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Lesson(models.Model):
    title = models.CharField(max_length=128)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    example_code = models.TextField()
    compiler_flags = models.CharField(max_length=FLAGS_MAXLEN, blank=True)

class User(models.Model):
    username = models.CharField(max_length=64, primary_key=True)
    password = models.CharField(max_length=128)
    enrolled_in = models.ManyToManyField(Course, blank=True)
    owned = models.ManyToManyField(Course, blank=True, related_name='owned_courses')
    completed_lessons = models.ManyToManyField(Lesson, blank=True)

class SolutionSet(models.Model):
    # index:
    # index/order that the tests will be run in.
    # this is here to enable the capability to say "you passed/failed test number 1"
    # and have it always refer to the same test
    index = models.IntegerField
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    stdin = models.TextField()
    stdout = models.TextField()

    class Meta:
        ordering = ['index']

class Submission(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    code = models.TextField()
    compiler_flags = models.CharField(max_length=FLAGS_MAXLEN)
    passed = models.BooleanField(default=False)
