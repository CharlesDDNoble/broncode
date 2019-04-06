from django.urls import path
from . import views

urlpatterns = [
    path('', views.thepage, name = 'the page'),
]
