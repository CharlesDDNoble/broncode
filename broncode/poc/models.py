from django.db import models

# Create your models here.

FLAGS_MAXLEN = 512

class Course(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    title = models.CharField(max_length=128)
    number = models.IntegerField()
    course = models.ForeignKey(Course, related_name='chapters', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['course', 'number']

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=128)
    number = models.IntegerField()
    chapter = models.ForeignKey(Chapter, related_name='lessons', on_delete=models.CASCADE)
    example_code = models.TextField()
    compiler_flags = models.CharField(max_length=FLAGS_MAXLEN, blank=True)

    class Meta:
        unique_together = ['chapter', 'number']

    def __str__(self):
        return self.title

class User(models.Model):
    username = models.CharField(max_length=64, primary_key=True)
    password = models.CharField(max_length=128)
    enrolled_in = models.ManyToManyField(Course, blank=True)
    owned_courses = models.ManyToManyField(Course, blank=True, related_name='owned_courses')
    completed_lessons = models.ManyToManyField(Lesson, blank=True)

class SolutionSet(models.Model):
    # number:
    # order that the tests will be run in.
    # this is here to enable the capability to say "you passed/failed test number 1"
    # and have it always refer to the same test
    number = models.IntegerField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    stdin = models.TextField()
    stdout = models.TextField()

    class Meta:
        unique_together = ['lesson', 'number']

class Submission(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    code = models.TextField()
    compiler_flags = models.CharField(max_length=FLAGS_MAXLEN)
    passed = models.BooleanField(default=False)
