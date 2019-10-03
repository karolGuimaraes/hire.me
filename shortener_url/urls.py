from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_shortener, name='create_shortener'),
    path('', views.retrieve_url, name='retrieve_url'),
    path('visited', views.visited_url, name='visited_url'),
]