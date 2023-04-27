from datetime import timedelta

from django.test import TestCase
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

from apps.mappings.models import Mapping


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


def create_mapping(user, **params):
    """Create and return a test mapping."""
    defaults = {
        'target': 'https://www.google.com',
        'expiry_date': None,
    }
    defaults.update(params)

    mapping = Mapping.objects.create(user=user, **defaults)
    return mapping


class MappingTests(TestCase):
    """Test Mapping model."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_create_mapping_successful(self):
        """Test creating a Mapping is successful."""
        mapping = create_mapping(
            user=self.user,
            target='http://www.example.com'
        )

        self.assertEqual(mapping.user, self.user)
        self.assertEqual(mapping.target, 'http://www.example.com')
        self.assertEqual(mapping.visits, 0)
        self.assertIsNone(mapping.expiry_date)

    def test_create_mapping_with_expiry_date_successful(self):
        """Test creating a Mapping with expiry date."""
        expiry_date = timezone.now() + timedelta(days=2)
        mapping = create_mapping(
            user=self.user,
            expiry_date=expiry_date
        )

        self.assertIsNotNone(mapping.expiry_date)
        self.assertEqual(mapping.expiry_date, expiry_date)

    def test_create_mapping_generates_key(self):
        """Test when creating a Mapping with no key, the key gets generated."""
        mapping = create_mapping(user=self.user)

        self.assertIsNotNone(mapping.key)
        self.assertEqual(len(mapping.key), settings.DEFAULT_KEY_LEN)
