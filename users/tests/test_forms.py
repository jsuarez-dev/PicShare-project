"""Tests of user's forms"""

# Django
from django.test import TestCase
# Forms

# Models
from users.models import User


class TestLoginForm(TestCase):
    """test the login form"""
    def setUp(self):
        """Initialise variables."""
        User.objects.create(
            username='john123',
            password='12345',
            first_name='john',
            last_name='smith',
            email='john@smith.io'
        )

    def test_basic_form(self):
        """check the basic functionality
         of the login from"""
        #form = LoginForm(
            #username='john123',
            #password='12345'
        #)

        #self.assertTrue(form.is_valid())