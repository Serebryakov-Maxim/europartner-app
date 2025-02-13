from django.contrib import admin
from django.urls import path
from . import views


app_name = 'sensors'

urlpatterns = [
    path('api/values/', views.ValuesSensorApiView.as_view(), name='api'),
    path('api/list_parameters/', views.ListParametersApiView.as_view(), name='api'),
    path('api/list_parameters_v2/', views.ListParameters_v2_ApiView.as_view(), name='api'),
    path('api/last_parameters/', views.LastParametersApiView.as_view(), name='api'),
    path('api/get_sensors/', views.SensorApiView.as_view(), name='api'),
]