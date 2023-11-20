from django.contrib import admin
from django.urls import path
from . import views


app_name = 'tpa'

urlpatterns = [
    path('', views.list, name='list'),
    path('api/', views.MachineListApiView.as_view(), name='api'),
]