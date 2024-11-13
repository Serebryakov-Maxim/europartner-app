from django.contrib import admin
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('ventilation/', views.ventilation, name='ventilation'),
    path('yandex_forms/', views.yandex_forms, name='yandex_forms'),
]