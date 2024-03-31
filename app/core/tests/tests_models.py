"""
Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_id_successful(self):
        """Test creating a user with an id is successful"""

        id = 'test@example.com'
        password = 'test@pass123'

        user = get_user_model().objects.create_user(
            id=id,
            password=password
        )

        self.assertEqual(user.id, id)
        self.assertTrue(user.check_password(password))


    def test_new_user_without_id_raises_error(self):
        """Test that creating a user without id raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test@123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'SU01',
            'test@pass'
        )
        self.assertTrue(user.is_superuser)
