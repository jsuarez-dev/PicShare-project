"""Login views unit test"""

# Django
from django.test import TestCase, Client
from django.urls import reverse
# Models
from users.models import User


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
        self.assertEquals(response.url, reverse('users:email_confirm_sent'))
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
        self.assertEquals(response.url, reverse('users:email_confirm_sent'))
        self.assertEquals(User.objects.get(username='john123').email, 'john@smith.io')

        response = self.client.post(self.url, {
            'username': 'john@smith.io',
            'password': '12345'
        })

        self.assertEquals(response.status_code, 302)
        self.assertIsNone(response.context)
