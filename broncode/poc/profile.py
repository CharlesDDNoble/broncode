from django.db import models
from django.contrib.auth.models import User
from poc.models import Course, Lesson

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=64, primary_key=True)
    password = models.CharField(max_length=128)
    enrolled_in = models.ManyToManyField(Course, blank=True)
    owned = models.ManyToManyField(Course, blank=True, related_name='owned_courses')
    completed_lessons = models.ManyToManyField(Lesson, blank=True)

    