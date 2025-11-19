from django.contrib import admin
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('ping/', views.ping, name='ping'),
    path('ventilation/', views.ventilation, name='ventilation'),
    path('yandex_forms/', views.yandex_forms, name='yandex_forms'),
    path('mqtt_publish/', views.mqtt_publish, name='mqtt_publish'),
]