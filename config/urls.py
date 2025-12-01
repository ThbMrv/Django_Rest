from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

# Swagger / OpenAPI (drf-yasg)
try:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
except Exception:
    SpectacularAPIView = SpectacularSwaggerView = SpectacularRedocView = None


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('concession.urls')),
]

# Expose OpenAPI docs with drf-spectacular if installed
if SpectacularAPIView is not None:
    urlpatterns += [
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('doc/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]

# During development serve the frontend static files from /frontend/
if settings.DEBUG:
    urlpatterns += [
        # Serve the index at the exact /frontend/ path first
        re_path(r'^frontend/?$', serve, kwargs={'path': 'index.html', 'document_root': str(settings.BASE_DIR / 'frontend')}),
        # Serve files under /frontend/<path> (require at least one char for path)
        re_path(r'^frontend/(?P<path>.+)$', serve, kwargs={'document_root': str(settings.BASE_DIR / 'frontend')}),
    ]
