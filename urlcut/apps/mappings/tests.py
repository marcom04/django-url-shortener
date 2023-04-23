"""
Test mappings.
"""

from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.core.models import Mapping


def forward_target_url(key):
    """Create and return a forward to target URL."""
    return reverse('mappings:forward', kwargs={'key': key})


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


class MappingViewTests(TestCase):
    """Test mapping views."""

    def setUp(self):
        self.client = Client()
        self.user = create_user(email='test@example.com', password='testpass123')

    def test_forward_to_target(self):
        """Test the redirect from key to target URL."""
        mapping = create_mapping(self.user)

        res = self.client.get(forward_target_url(mapping.key))
        self.assertRedirects(res, mapping.target, fetch_redirect_response=False)

    def test_increment_visits_after_forward(self):
        """Test that a forward increments the visits count."""
        mapping = create_mapping(self.user)

        self.client.get(forward_target_url(mapping.key))
        mapping.refresh_from_db(fields=['visits'])
        self.assertEqual(mapping.visits, 1)

    def test_forward_to_expired_target(self):
        """Test that visiting an expired mapping does not work."""
        mapping = create_mapping(self.user, expiry_date=timezone.now())

        res = self.client.get(forward_target_url(mapping.key))
        self.assertEqual(res.status_code, 404)

    # TODO: test task delete expired mappings
    # Test 1: test that the task is called with correct parameters
    # Test 2: test the task as a normal function by calling it
