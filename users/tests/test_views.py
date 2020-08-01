"""Django view tests"""

# Django
from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils import timezone
from django.conf import settings
# Models
from users.models import User
from users.models import Profile
# Utilities
import jwt
from datetime import timedelta


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


class TestLoginView(TestCase):
    """Test the functionality of the Login view"""
    def setUp(self):
        """Initialise variables."""
        self.client = Client()
        self.url = reverse('users:login')

    def test_basic_login_username(self):
        """Test basic login username"""
        response = self.client.post(reverse('users:signup'), {
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

        response = self.client.post(self.url, {
            'username': 'john123',
            'password': '12345'
        })

        self.assertEquals(response.status_code, 302)
        self.assertIsNone(response.context)

    def test_basic_login_email(self):
        """Test basic login email"""
        response = self.client.post(reverse('users:signup'), {
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

        response = self.client.post(self.url, {
            'username': 'john@smith.io',
            'password': '12345'
        })

        self.assertEquals(response.status_code, 302)
        self.assertIsNone(response.context)


class TestVerifyView(TestCase):
    """Test verify view"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('users:signup')

        self.client.post(self.url, {
            'username': 'john123',
            'password': '12345',
            'password_confirmation': '12345',
            'first_name': 'john',
            'last_name': 'smith',
            'email': 'john@smith.io'
        })

    def test_normal_view(self):
        """Verify with an usual username"""
        token = self.generate_verification_token('john123')
        url = '/users/email/verify/?token={}'.format(token)
        response = self.client.get(url)
        user = User.objects.get(username='john123')
        self.assertTrue(user.is_verified)

    def generate_verification_token(self, username):
        """ Create JWT token that he user can use to verify its account """
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return token.decode()

