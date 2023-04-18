"""
URL mappings for the mapping API.
"""
from django.urls import path

from . import views


app_name = 'mappings'

urlpatterns = [
    path('shorten/', views.ShortenURLApiView.as_view(), name='shorten'),
    path('keys/<str:key>/', views.RetrieveMappingApiView.as_view(), name='key-detail'),
    path('keys/', views.ListMappingsApiView.as_view(), name='key-list'),
]
