"""
urlcut URL Configuration
"""
from django.contrib import admin
from django.urls import (
    path,
    include,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # REST API URLs
    path('api/v1/', include('api.urls', namespace='api')),

    path('', include('apps.mappings.urls')),
]
