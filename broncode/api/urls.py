from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.api_root),
    path('users/', views.UserList.as_view(), name='users-list'),
    path('users/<str:username>/', views.UserDetail.as_view())
]
