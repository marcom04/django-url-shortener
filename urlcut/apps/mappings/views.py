import logging

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView

from apps.core.models import Mapping
from .forms import CreateMappingForm

app_log = logging.getLogger('urlcut.apps.mappings')


@login_required
def shorten_url(request):
    """
    Create a Mapping for a target URL provided via form.
    """
    form = CreateMappingForm(request.POST or None)
    context = {
        'form': form
    }

    if request.method == 'POST':
        if form.is_valid():
            mapping = form.save(commit=False)
            mapping.user = request.user
            mapping.save()
            context['mapping'] = mapping
            context['short_url'] = f"{request.build_absolute_uri('/')}{mapping.key}"

    return render(
        request,
        'mappings/index.html',
        context
    )


class ForwardToTargetView(RedirectView):
    """Given a Mapping key, redirect the user to the related target URL."""

    def get_redirect_url(self, *args, **kwargs):
        key = kwargs.get('key')
        mapping = get_object_or_404(Mapping.actives, key=key)
        mapping.increment_visits()
        return mapping.target
