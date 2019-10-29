from django.urls import path
from poc import views

urlpatterns = [
    path('', views.index, name = 'homepage'),
    path('course/', views.createCourse, name = 'create_course'),
    path(r'lesson/(?P<slug>[-\w]+)/$', views.createLesson, name = 'create_lesson'),
    path('lesson/<int:lesson_id>/', views.lesson, name = 'lesson'),
    path('register/', views.register, name = 'register'),
]
