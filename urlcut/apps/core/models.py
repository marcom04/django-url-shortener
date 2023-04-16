from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)


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


class User(AbstractUser):
    """
    A user in the system, having the e-mail as username.
    """
    email = models.EmailField(max_length=255, unique=True)

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'user'


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

    class Meta:
        db_table = 'mapping'

    @property
    def is_active(self):
        return self.expiry_date is None or timezone.now() < self.expiry_date

    def __str__(self):
        return self.key

    def increment_visits(self):
        # TODO: increment visits field using F() to avoid race conditions
        pass
