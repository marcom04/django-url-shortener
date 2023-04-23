from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.core.models import Mapping


class CreateMappingSerializer(serializers.ModelSerializer):
    """Serializer for the shortener (create mapping) view."""
    class Meta:
        model = Mapping
        fields = ['user', 'target', 'key', 'expiry_date']
        read_only_fields = ['user', 'key']

    def to_representation(self, instance):
        """Add full short_url for reading ops."""
        ret = super().to_representation(instance)
        ret['short_url'] = f"{self.context.get('request').build_absolute_uri('/')}{instance.key}"
        return ret

    def validate(self, attrs):
        if 'expiry_date' in attrs and attrs['expiry_date'] is not None and attrs['expiry_date'] <= timezone.now():
            raise serializers.ValidationError({
                'expiry_date': _('Expiry date cannot be in the past')
            })
        return attrs


class MappingSerializer(serializers.ModelSerializer):
    """Serializer for mapping listing and retrieval."""
    class Meta:
        model = Mapping
        fields = ['target', 'key', 'expiry_date', 'visits']

    def to_representation(self, instance):
        """Add is_active flag for reading ops."""
        ret = super().to_representation(instance)
        ret['is_active'] = instance.is_active
        return ret
