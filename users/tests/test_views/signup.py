"""Unit test sign up"""
# Django
from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
# Models
from users.models import User


class TestSignUpViews(TestCase):
    """Test the functionality of the SignIn view"""
    def setUp(self):
        """Initialise variables."""
        self.client = Client()
        self.url = reverse('users:signup')

    def test_normal_signup(self):
        """Usual sing up"""
        response = self.client.post(self.url, {
            'username': 'john123',
            'password': '12345',
            'password_confirmation': '12345',
            'first_name': 'john',
            'last_name': 'smith',
            'email': 'john@smith.io'
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('users:send_email_verification'))
        self.assertEquals(User.objects.get(username='john123').email, 'john@smith.io')

    def test_black_signup(self):
        response = self.client.post(self.url, {})
        self.assertGreaterEqual(len(response.context['form'].errors), 1)

    def test_signup_different_password(self):
        response = self.client.post(self.url, {
            'username': 'john123',
            'password': '12345',
            'password_confirmation': 'nosame',
            'first_name': 'john',
            'last_name': 'smith',
            'email': 'john@smith.io'
        })
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username='john123')

        self.assertGreaterEqual(len(response.context['form'].errors), 1)