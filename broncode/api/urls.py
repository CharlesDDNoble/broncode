from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('users/', views.user_list),
    path('users/<str:username>/', views.user_detail)
]
