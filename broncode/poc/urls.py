from django.urls import path
from poc import views

urlpatterns = [
    path('', views.index, name = 'homepage'),
    path('course/', views.course, name = 'course'),
    path('course/<int:course_id>/', views.lessonList, name = 'lesson_list'),
    path('course/<int:course_id>/createLesson/', views.createLesson, name = 'create_lesson'),
    path('lesson/<int:lesson_id>/', views.lesson, name = 'lesson'),
    path('register/', views.register, name = 'register'),
]
