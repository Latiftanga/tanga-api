"""Test for the user API"""
from django.test import TestCase
from django.urls import reverse

from core.models import Teacher

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('teacher:create')

def create_teacher(**params):
    """Create and return a new user"""
    return Teacher.objects.create(**params)


class PublicUserAPITests(TestCase):
    """Test the public features of the Teacher API"""

    def setUp(self):
        self.client = APIClient()



