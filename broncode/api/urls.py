from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='broncode api'),
    path('users/', views.ListUsersView.as_view(), name='users-all')
]
