from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_shortener, name='create_shortener'),
    path('', views.retrieve_url, name='retrieve_url'),
    path('top_visited', views.top_urls_visited, name='top_urls_visited'),
    path('urls', views.urls, name='urls'),
]