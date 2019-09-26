from django.urls import path
from poc import views

urlpatterns = [
    path('', views.index, name = 'homepage'),
    path('main/', views.main, name = 'mainpage'),
    path('tutorial/', views.tutorial, name = 'tutorial'),
]
