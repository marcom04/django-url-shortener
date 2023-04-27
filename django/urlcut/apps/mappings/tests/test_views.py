"""
Test mappings.
"""
from datetime import timedelta

from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core import mail

from apps.mappings.models import Mapping
from apps.mappings.tasks import cleanup_mappings


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

    def test_cleanup_mappings(self):
        """Test the cleanup mappings task deletes expired mappings."""
        create_mapping(self.user, expiry_date=timezone.now())

        deleted = cleanup_mappings()
        self.assertEqual(deleted, 1)
        self.assertEqual(Mapping.objects.count(), 0)

    def test_cleanup_only_expired_mappings(self):
        """Test the cleanup mappings tasks deletes only expired mappings."""
        create_mapping(self.user)
        create_mapping(self.user, expiry_date=timezone.now() + timedelta(days=2))
        expired = create_mapping(self.user, expiry_date=timezone.now())

        deleted = cleanup_mappings()
        self.assertEqual(deleted, 1)
        self.assertEqual(Mapping.objects.count(), 2)
        self.assertFalse(Mapping.objects.filter(id=expired.id).exists())

    def test_cleanup_mappings_email_to_users(self):
        """Test the notification is sent to users whose expired mappings are deleted."""
        create_mapping(user=self.user, expiry_date=timezone.now())

        deleted = cleanup_mappings()
        self.assertEqual(deleted, 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user.email])
        self.assertIn('Expired URLs', mail.outbox[0].subject)

    def test_cleanup_mappings_email_to_users_grouped_by_user(self):
        """Test the expired notification is sent only once per user."""
        user2 = create_user(email='test2@example.com', password='testpass123')
        create_mapping(user=self.user, expiry_date=timezone.now())
        create_mapping(user=self.user, expiry_date=timezone.now())
        create_mapping(user=user2, expiry_date=timezone.now())

        deleted = cleanup_mappings()
        self.assertEqual(deleted, 3)
        self.assertEqual(len(mail.outbox), 2)

    def test_cleanup_guest_mappings(self):
        """Test the cleanup mappings task deletes expired guest mappings."""
        create_mapping(user=None, expiry_date=timezone.now())

        deleted = cleanup_mappings()
        self.assertEqual(deleted, 1)
        self.assertEqual(Mapping.objects.count(), 0)

    def test_cleanup_guest_mappings_no_email_notification(self):
        """Test the expired notification is not sent when deleting guest mappings."""
        create_mapping(user=None, expiry_date=timezone.now())

        deleted = cleanup_mappings()
        self.assertEqual(deleted, 1)
        self.assertEqual(len(mail.outbox), 0)
