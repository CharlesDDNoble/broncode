from django.contrib import admin
import models

# Register your models here.
admin.site.register(models.Course)
admin.site.register(models.Chapter)
admin.site.register(models.Lesson)
admin.site.register(models.User)
admin.site.register(models.SolutionSet)
admin.site.register(models.Submission)
