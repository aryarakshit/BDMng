from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',        include('apps.dashboard.urls',   namespace='dashboard')),
    path('donors/', include('apps.donors.urls',    namespace='donors')),
    path('inventory/', include('apps.inventory.urls', namespace='inventory')),
    path('requests/', include('apps.blood_requests.urls', namespace='requests')),
    path('donations/', include('apps.donations.urls', namespace='donations')),
    path('reports/', include('apps.reports.urls',  namespace='reports')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
