from django.urls import path
from poc import views

urlpatterns = [
    path('', views.index, name = 'homepage'),
    path('main/', views.main, name = 'mainpage'),
    path('chapter/', views.createChapter, name = 'create_chapter')
    path('lesson/', views.createLesson, name = 'create_lesson')
    path('lesson/<int:lesson_id>/', views.lesson, name = 'lesson'),
    path('register/', views.register, name = 'register'),
]
