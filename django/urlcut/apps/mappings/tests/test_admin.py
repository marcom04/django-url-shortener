from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

from apps.mappings.models import Mapping


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )
        self.mapping = Mapping.objects.create(
            user=self.user,
            target='http://www.example.com'
        )

    def test_mapping_list(self):
        """Test that mappings are listed on page."""
        url = reverse('admin:mappings_mapping_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.mapping.target)
        self.assertContains(res, self.mapping.key)
