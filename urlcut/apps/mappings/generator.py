import secrets
import string

from django.conf import settings

from apps.core.models import Mapping


def create_random_key(length=settings.DEFAULT_KEY_LEN):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key(length=settings.DEFAULT_KEY_LEN):
    new_key = create_random_key(length)
    while Mapping.objects.filter(key=new_key).exists():
        new_key = create_random_key(length)
    return new_key


def generate_mapping(user, target):
    mapping = Mapping.objects.create(
        user=user,
        target=target,
        key=create_unique_random_key()
    )
    return mapping
