import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView

from api.mappings.serializers import (
    CreateMappingSerializer,
    MappingSerializer,
)
from apps.core.models import Mapping

app_log = logging.getLogger('urlcut.apps.api')


class ShortenURLApiView(CreateAPIView):
    """
    Shorten a given URL, and optionally set an expiration date on the link.
    """
    serializer_class = CreateMappingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveMappingApiView(RetrieveAPIView):
    """
    Get information about a given mapping key belonging to the authenticated user.
    """
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'key'
    lookup_url_kwarg = 'key'

    def get_queryset(self):
        return Mapping.objects.filter(user=self.request.user)


class ListMappingsApiView(ListAPIView):
    """
    Get the list of mappings for the authenticated user.
    """
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Mapping.objects.filter(user=self.request.user)
