from django.contrib import admin
from django.urls import path
from . import views


app_name = 'tpa'

urlpatterns = [
    path('', views.list, name='list'),
    path('<int:machine_id>', views.machine_card, name='machine_card'),
    path('<int:machine_id>/last_data/', views.machine_last_data, name='machine_last_data'),
    path('<int:machine_id>/job/', views.machine_job, name='machine_job'),
    path('api/machine/', views.MachineListApiView.as_view(), name='api'),
    path('api/job/', views.JobListApiView.as_view(), name='api'),
    path('api/cycle/', views.CycleApiView.as_view(), name='api'),
    path('api/cycle/list/', views.CycleApiView.as_view(), name='api'),
    path('api/quantity_by_job/', views.QuantProdApiView.as_view(), name='api'),
    path('api/event/', views.EventApiView.as_view(), name='api'),
    path('api/effect_cycle/', views.EffectCycleApiView.as_view(), name='api'),
    path('api/time_cycle_by_job/', views.TimeProdApiView.as_view(), name='api'),
    path('api/first_cycle_by_job/', views.FirstCycleOnDateApiView.as_view(), name='api'),
    path('api/last_cycle_by_job/', views.LastCycleOnDateApiView.as_view(), name='api'),
]