from django.contrib import admin
from django.urls import path
from . import views


app_name = 'tpa'

urlpatterns = [
    path('', views.list, name='list'),
    path('<int:machine_id>', views.machine_card, name='machine_card'),
    path('api/machine/', views.MachineListApiView.as_view(), name='api'),
    path('api/job/', views.JobListApiView.as_view(), name='api'),
]