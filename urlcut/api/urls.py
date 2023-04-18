from django.urls import (
    path,
    include,
)
from drf_spectacular.views import (
    SpectacularSwaggerView,
    SpectacularAPIView,
)

app_name = 'api'

urlpatterns = [
    path('doc/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
    path('schema/', SpectacularAPIView.as_view(api_version='v1'), name='schema'),
    path('mappings/', include('api.mappings.urls')),
    path('users/', include('api.users.urls')),
]
