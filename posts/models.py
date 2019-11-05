"""Post models."""

# Django
from django.db import models


class User(models.Model):
    """User model"""

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    bio = models.TextField()

    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)

    is_admin = models.BooleanField(default=False)

    birth_date = models.DateField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
