"""
Tests for the mappings API.
"""
import logging
from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from apps.mappings.models import Mapping

logging.disable(logging.CRITICAL)


CREATE_MAPPING_URL = reverse('api:mappings:shorten')
CREATE_GUEST_MAPPING_URL = reverse('api:mappings:guest-shorten')
KEY_LIST_URL = reverse('api:mappings:key-list')


def key_detail_url(key):
    return reverse('api:mappings:key-detail', kwargs={'key': key})


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


class PublicUserApiTests(TestCase):
    """Test the public features of the mappings API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_guest_mapping_success(self):
        """Test successful creation of anonymous (guest) mapping."""
        payload = {
            'target': 'https://www.google.com'
        }
        res = self.client.post(CREATE_GUEST_MAPPING_URL, payload)
        in_24_hrs = timezone.now() + timedelta(days=1)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('key', res.data)
        self.assertIn('short_url', res.data)
        self.assertTrue(len(res.data['short_url'].strip()) > 0)
        self.assertEqual(Mapping.objects.count(), 1)
        mapping = Mapping.objects.first()
        self.assertEqual(mapping.target, payload['target'])
        self.assertIsNone(mapping.user)
        self.assertTrue(mapping.is_active)
        self.assertAlmostEqual(
            mapping.expiry_date, in_24_hrs, delta=timedelta(minutes=1)
        )

    def test_create_mapping_unauthorized(self):
        """Test authentication is required to create a mapping with full functionalities."""
        res = self.client.post(CREATE_MAPPING_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_of_mappings_unauthorized(self):
        """Test authentication is required to get the list of mappings."""
        res = self.client.get(KEY_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_mapping_success(self):
        """Test successful creation of mapping without expiry date as parameter."""
        payload = {
            'target': 'https://www.google.com'
        }
        res = self.client.post(CREATE_MAPPING_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('key', res.data)
        self.assertIn('short_url', res.data)
        self.assertTrue(len(res.data['short_url'].strip()) > 0)
        self.assertEqual(Mapping.objects.count(), 1)
        mapping = Mapping.objects.first()
        self.assertEqual(mapping.target, payload['target'])
        self.assertEqual(mapping.user, self.user)
        self.assertTrue(mapping.is_active)

    def test_create_mapping_with_empty_expiry_date(self):
        """Test successful creation of mapping passing empty expiry date."""
        payload = {
            'target': 'https://www.google.com',
            'expiry_date': ''
        }
        res = self.client.post(CREATE_MAPPING_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        mapping = Mapping.objects.first()
        self.assertIsNone(mapping.expiry_date)
        self.assertTrue(mapping.is_active)

    def test_create_mapping_with_valid_expiry_date(self):
        """Test successful creation of mapping with expiry date."""
        payload = {
            'target': 'https://www.google.com',
            'expiry_date': timezone.now() + timedelta(days=1)
        }
        res = self.client.post(CREATE_MAPPING_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        mapping = Mapping.objects.first()
        self.assertEqual(mapping.expiry_date, payload['expiry_date'])
        self.assertTrue(mapping.is_active)

    def test_create_mapping_with_invalid_expiry_date(self):
        """Test that creation of mapping with expiry date in the past doesn't work."""
        payload = {
            'target': 'https://www.google.com',
            'expiry_date': timezone.now() - timedelta(days=1)
        }
        res = self.client.post(CREATE_MAPPING_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_list_of_mappings(self):
        """Test getting the list of mappings for the authenticated user."""
        create_mapping(self.user)
        create_mapping(self.user)

        res = self.client.get(KEY_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('count', res.data)
        self.assertEqual(res.data['count'], 2)

    def test_get_list_of_mapping_limited_to_user(self):
        """Test that the list of mappings contains only mappings of the authenticated user."""
        user2 = create_user(
            email='test2@example.com',
            password='testpass123',
            name='Test Name 2',
        )
        create_mapping(self.user)
        create_mapping(self.user)
        create_mapping(user2)

        res = self.client.get(KEY_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 2)

    def test_get_mapping_detail(self):
        """Test getting the detail of a mapping of the authenticated user."""
        m = create_mapping(self.user)

        res = self.client.get(key_detail_url(m.key))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(m.key, res.data['key'])

    def test_get_mapping_detail_non_existing(self):
        """Test getting the detail of a non-existing key returns error."""
        res = self.client.get(key_detail_url('asdfasdf'))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_mapping_detail_of_other_user(self):
        """Test getting the detail of a mapping belonging to another user returns error."""
        user2 = create_user(
            email='test2@example.com',
            password='testpass123',
            name='Test Name 2',
        )
        m = create_mapping(user2)

        res = self.client.get(key_detail_url(m.key))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
