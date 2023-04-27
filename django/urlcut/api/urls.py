from django.urls import (
    path,
    include,
)
from drf_spectacular.views import (
    SpectacularSwaggerView,
    SpectacularAPIView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    path('doc/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
    path('schema/', SpectacularAPIView.as_view(api_version='v1'), name='schema'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('mappings/', include('api.mappings.urls', namespace='mappings')),
    path('users/', include('api.users.urls', namespace='users')),
]
