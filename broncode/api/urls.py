from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'chapters', views.ChapterViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'submissions', views.SubmissionViewSet)

urlpatterns = [
    path('', include(router.urls))
]
