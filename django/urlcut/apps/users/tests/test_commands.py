"""
Test custom Django management commands.
"""

from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model


class CommandTests(TestCase):
    """Test commands."""

    def test_ensure_superuser_create(self):
        """Test that a non-existing superuser is created."""
        call_command('ensure_superuser', email='admin@example.com', password='testpass123')

        users = get_user_model().objects.filter(email='admin@example.com')
        self.assertTrue(users.exists())
        user = users.first()
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_superuser)

    def test_ensure_superuser_found(self):
        """Test that an existing superuser is not created."""
        get_user_model().objects.create_superuser(email='admin@example.com', password='testpass123')
        call_command('ensure_superuser', email='admin@example.com', password='testpass123')

        self.assertEqual(get_user_model().objects.count(), 1)
