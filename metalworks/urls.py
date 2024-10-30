from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'metalworks'

urlpatterns = [
    path('', views.details, name='details'),
    path('create/', views.create, name='create'),
    path('history/', views.history, name='history'),
    path('production/', views.production, name='production'),
    path('operation/', views.operation, name='operation'),
    path('<int:detail_id>', views.card, name='card'),
    path('api/detail/', views.DetailApiView.as_view(), name='api'),
    path('api/last_modified/', views.DetailLastModifiedApiView.as_view(), name='api'),
]