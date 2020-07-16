"""Users model"""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User model.
    User extend from
    """

    email = models.EmailField(
        'email address',
        unique=True,
        max_length=254,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user have verified its email.'
    )

    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['username']

    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username
