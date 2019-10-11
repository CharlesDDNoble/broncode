from django.contrib import admin
from .models import Course
from .models import Chapter
from .models import Lesson
from .models import UserProfile
from .models import SolutionSet
from .models import Submission

# Register your models here.
admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Lesson)
admin.site.register(UserProfile)
admin.site.register(SolutionSet)
admin.site.register(Submission)
