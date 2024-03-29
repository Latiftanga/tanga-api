"""
Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""

        email = 'test@example.com'
        password = 'test@pass123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@eg.com', 'test1@eg.com'],
            ['Test2@Eg.com', 'Test2@eg.com'],
            ['TEST3@EG.COM', 'TEST3@eg.com'],
            ['test4@eg.COM', 'test4@eg.com']
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample@pass')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test@123')

    def test_create_user_user(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@eg.eg.com',
            'test@pass'
        )
        self.assertTrue(user.is_superuser)
