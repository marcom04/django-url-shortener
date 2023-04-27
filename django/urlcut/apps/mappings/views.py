import logging

from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

from apps.mappings.models import Mapping

app_log = logging.getLogger('urlcut.apps.mappings')


class ForwardToTargetView(RedirectView):
    """Given a Mapping key, redirect the user to the related target URL."""

    def get_redirect_url(self, *args, **kwargs):
        key = kwargs.get('key')
        mapping = get_object_or_404(Mapping.objects.active(), key=key)
        mapping.increment_visits()
        return mapping.target
