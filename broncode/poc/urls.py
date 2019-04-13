from django.urls import path
from poc import views

urlpatterns = [
    path('', views.index, name = 'the page'),
]
