from django.contrib import admin
from django.urls import path,include, re_path
from .views import post_home


urlpatterns = [
    path('', post_home),
]

