from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<str:username>/', views.UserDetail.as_view())
]
