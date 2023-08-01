from django.contrib import admin
from django.urls import path
from . import views

app_name = 'pressforms'

urlpatterns = [
    path('', views.pressforms, name='pressforms'),
    path('create/', views.create, name='create'),
    path('history/', views.history, name='history'),
    path('production/', views.production, name='production'),
    path('operation/', views.operation, name='operation'),
    path('<int:pressform_id>', views.card, name='card'),
]