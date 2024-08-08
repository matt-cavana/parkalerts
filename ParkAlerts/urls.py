# ParkAlerts/urls.py
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from alerts import views as alert_views  # Import the views from the alerts app
from alerts.views import test_email # delete after testing
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', alert_views.home_page, name='home_page'),  # Set the new home page as default
    path('alerts/', include('alerts.urls')),  # Regular views under 'alerts/'
    path('', include('alerts.urls')),  # This line ensures that the alerts URLs are included in the root URL patterns
    path('create_alert/', alert_views.create_alert, name='create_alert'),
    path('api/', include('alerts.api_urls')),  # API endpoints under 'api/'
    path('test-email/', test_email, name='test_email'),  # delete after testing
    # path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add this for serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
