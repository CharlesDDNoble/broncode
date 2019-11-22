from django.urls import path
from poc import views

urlpatterns = [
    path('', views.index, name = 'homepage'),
    path('course/', views.course, name = 'course'),
    path('course/<int:course_id>/', views.lessonList, name = 'lesson_list'),
    path('course/<int:course_id>/create-lesson/', views.createLesson, name = 'create_lesson'),
    path('course/<int:course_id>/edit-lesson/<int:lesson_number>', views.editLesson, name = 'edit_lesson'),
    path('course/<int:course_id>/lesson/<int:lesson_number>/', views.lesson, name = 'lesson'),
    path('register/', views.register, name = 'register'),
]
