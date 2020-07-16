"""User Models"""

# Django
from django.db import models
from django.core.validators import RegexValidator
# Models
from users.models import User


class Profile(models.Model):
    """Profile model.
    We use proxy model that extends the base data with
    other information
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='Phone number must be in the format +99999999. Up to 15 digits allowed'
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=15,
        unique=True,
        null=True,
        blank=True
    )

    picture = models.ImageField(upload_to='users/pictures', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return username"""
        return self.user.username

