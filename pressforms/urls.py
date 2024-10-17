from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'pressforms'

urlpatterns = [
    path('', views.pressforms, name='pressforms'),
    path('create/', views.create, name='create'),
    path('history/', views.history, name='history'),
    path('production/', views.production, name='production'),
    path('operation/', views.operation, name='operation'),
    path('media/', views.media, name='media'),
    path('gantt/', views.gantt, name='gantt'),
    path('<int:pressform_id>', views.card, name='card'),
    path('api/list/', views.PressformApiView.as_view(), name='api'),
    path('api/last_modified/', views.PressformLastModifiedApiView.as_view(), name='api'),
]