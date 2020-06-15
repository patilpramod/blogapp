from django.contrib import admin
from django.urls import path,include, re_path
from . import views


urlpatterns = [

    path('', views.post_list, name='list'),
    path('create', views.post_create),
    path('<int:id>/delete', views.post_delete),
    path('<int:id>/', views.post_detail, name='detail'),
    path('<int:id>/edit', views.post_update, name='update'),
]

