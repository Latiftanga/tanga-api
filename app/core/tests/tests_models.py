"""
Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an id is successful"""

        email = 'test@example.com'
        password = 'test@pass123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without id raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test@123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'super@eg.com',
            'test@pass'
        )
        self.assertTrue(user.is_superuser)

    def test_create_teacher_and_student_pins(self):
        """Test create pin(s) for students and teachers"""
        pin = models.PIN.objects.create(
            pin_type='teacher'
        )
        print(pin.pin_code)
        self.assertEqual(pin.pin_type, 'teacher')
