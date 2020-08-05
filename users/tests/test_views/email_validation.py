"""Email validation test views"""
# Django
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
# Models
from users.models import User
# Utilities
import jwt
from datetime import timedelta


def generate_verification_expired_token(username):
    """ Create JWT token that he user can use to verify its account """
    exp_date = timezone.now() - timedelta(days=3)
    payload = {
        'user': username,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token.decode()


def generate_verification_token(username):
    """ Create JWT token that he user can use to verify its account """
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': username,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token.decode()


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

    def test_verify_view_normal(self):
        """Verify with an usual username"""
        token = generate_verification_token('john123')
        url = '/users/email/verify/?token={}'.format(token)
        response = self.client.get(url)
        user = User.objects.get(username='john123')
        self.assertTrue(user.is_verified)
        self.assertEquals(response.context['status'], 'successful')

    def test_verify_view_empty_token(self):
        """Verify with an empty token"""
        token = ''
        url = '/users/email/verify/?token={}'.format(token)
        response = self.client.get(url)
        self.assertEquals(response.url, reverse('users:login'))

    def test_verify_view_fake_token(self):
        """Verify with an fake token"""
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        url = '/users/email/verify/?token={}'.format(token)
        response = self.client.get(url)
        self.assertEquals(response.url, reverse('users:login'))

    def test_verify_view_fake_user(self):
        """Verify with an fake user"""
        token = generate_verification_token('johan')
        url = '/users/email/verify/?token={}'.format(token)
        response = self.client.get(url)
        self.assertEquals(response.url, reverse('users:login'))

    def test_verify_view_expire_token(self):
        """Verify with an expire_token"""
        token = generate_verification_expired_token('john123')
        url = '/users/email/verify/?token={}'.format(token)
        response = self.client.get(url)
        user = User.objects.get(username='john123')
        self.assertFalse(user.is_verified)
        self.assertEquals(response.context['status'], 'Token has expired')

    def test_verify_view_user_already_verify(self):
        """Verify user already verify"""
        self.client.post(self.url, {
            'username': 'steve123',
            'password': '12345',
            'password_confirmation': '12345',
            'first_name': 'steve',
            'last_name': 'smith',
            'email': 'steve@steve.io'
        })
        token = generate_verification_token('steve123')
        url = '/users/email/verify/?token={}'.format(token)
        user = User.objects.get(username='steve123')
        user.is_verified = True
        user.save()
        response = self.client.get(url)
        self.assertEquals(response.url, reverse('users:login'))