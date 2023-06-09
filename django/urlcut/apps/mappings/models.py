import secrets
import string

from django.db import models
from django.db.models import (
    F,
    Q,
)
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone


def create_random_key(length=settings.DEFAULT_KEY_LEN):
    """
    Generate a random alphanumeric string of specified length, default to settings.DEFAULT_KEY_LEN.
    """
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key(length=settings.DEFAULT_KEY_LEN):
    """
    Generate a random string of specified length, making sure it does not already exist among Mappings' keys.
    """
    new_key = create_random_key(length)
    while Mapping.objects.filter(key=new_key).exists():
        new_key = create_random_key(length)
    return new_key


class MappingQuerySet(models.QuerySet):
    """Mappings custom queryset."""

    def active(self):
        return self.filter(
            Q(expiry_date__isnull=True) | Q(expiry_date__gt=timezone.now())
        )

    def expired(self):
        return self.filter(
            expiry_date__lte=timezone.now()
        )


class Mapping(models.Model):
    """
    A mapping between a target URL and a unique key.
    The key will compose the shortened URL.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mappings',
        verbose_name=_('User'),
        blank=True, null=True
    )

    target = models.URLField(verbose_name=_('Target URL'))
    key = models.CharField(max_length=10, unique=True,
                           db_index=True, verbose_name=_('Key'))
    visits = models.PositiveIntegerField(
        default=0, verbose_name=_('Number of visits'))
    created_at = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(
        blank=True, null=True, verbose_name=_('Expiry date'))

    objects = MappingQuerySet.as_manager()

    class Meta:
        db_table = 'mapping'

    @property
    def is_active(self):
        return self.expiry_date is None or timezone.now() < self.expiry_date

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = create_unique_random_key()
        super().save(*args, **kwargs)

    def increment_visits(self):
        # increment visits field using F() to avoid race conditions - the update is done at DB
        self.visits = F('visits') + 1
        self.save()
