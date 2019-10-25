from django.urls import path
from poc import views

urlpatterns = [
    path('', views.index, name = 'homepage'),
    path('main/', views.main, name = 'mainpage'),
    path('lesson/<int:lesson_id>/', views.lesson, name = 'lesson'),
    path('register/', views.register, name = 'register'),
]
