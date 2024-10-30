
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'partners'

urlpatterns = [
    path('api/partner/', views.PartnerApiView.as_view(), name='api'),
]