from django import forms
from django.utils.translation import gettext_lazy as _

from apps.core.models import Mapping


class CreateMappingForm(forms.ModelForm):
    target = forms.URLField(label=_('Your long URL'))

    class Meta:
        model = Mapping
        fields = ['target', 'expiry_date']
