from django.contrib import admin
from django.urls import path,include, re_path
from . import views


urlpatterns = [

    path('', views.post_list),
    path('create', views.post_create),
    path('delete', views.post_delete),
    path('<int:id>/', views.post_detail, name='detail'),
    path('update', views.post_update),
]

