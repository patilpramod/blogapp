from django.contrib import admin
from django.urls import path,include, re_path
from . import views


urlpatterns = [

    path('', views.post_list, name='list'),
    path('create', views.post_create),
    path('<slug:slug_id>/delete', views.post_delete),
    path('<slug:slug_id>/', views.post_detail, name='detail'),
    path('<slug:slug_id>/edit', views.post_update, name='update'),
  #  path('<str:id>/edit', views.post_update, name='update'),
]

