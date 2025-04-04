from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('main.urls')),
    path('pressforms/', include('pressforms.urls')),
    path('tpa/', include('tpa.urls')),
    path('partners/', include('partners.urls')),
    path('metalworks/', include('metalworks.urls')),
    path('sensors/', include('sensors.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
