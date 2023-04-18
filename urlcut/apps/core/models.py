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
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


def create_random_key(length=settings.DEFAULT_KEY_LEN):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key(length=settings.DEFAULT_KEY_LEN):
    new_key = create_random_key(length)
    while Mapping.objects.filter(key=new_key).exists():
        new_key = create_random_key(length)
    return new_key


class UserManager(BaseUserManager):
    """Manager for users with email as username."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'user'


class ActiveMappingManager(models.Manager):
    """
    Manager pre-filtering active mappings.
    """
    def get_queryset(self):
        return super().get_queryset().filter(
            Q(expiry_date__isnull=True) | Q(expiry_date__gt=timezone.now())
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
        verbose_name=_('User')
    )

    target = models.URLField(verbose_name=_('Target URL'))
    key = models.CharField(max_length=10, unique=True,
                           db_index=True, verbose_name=_('Key'))
    visits = models.PositiveIntegerField(
        default=0, verbose_name=_('Number of visits'))
    created_at = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(
        blank=True, null=True, verbose_name=_('Expiry date'))

    objects = models.Manager()
    actives = ActiveMappingManager()

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
        # increment visits field using F() to avoid race conditions
        self.visits = F('visits') + 1
        self.save()
