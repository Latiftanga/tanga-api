"""Test for User API"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

TOKEN_URL = reverse('core:token')
ME_URL = reverse('core:me')


class PublicUserAPITests(TestCase):
    """Test the public features of the Core API"""
    def setUp(self):
        self.client = APIClient()

    def test_create_token(self):
        """Test generate token for valid credentials"""
        user_details = {
            'email': 'email@eg.com',
            'password': 'test@pass123'
        }
        get_user_model().objects.create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_bad_credentials(self):
        """Test reuturn error if credentials are bad"""
        payload = {'email': '', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns error"""
        payload = {'email': 'USER01', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_aunauthorised(self):
        """Test authentication is required for users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test API request that require authentication"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='example@eg.com',
            password='test@pass'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def retrieving_user_profile_success(self):
        """Test retrieving login user profile is successful"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {'email': self.user.mail})

    def test_post_me_not_allowed(self):
        """Test POST method not allowed for the me endpoint"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'email': 'user@eg.com', 'password': 'test@pass'}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, payload['email'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
