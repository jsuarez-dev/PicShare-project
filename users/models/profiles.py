"""User Models"""

# Django
from django.db import models
# Models
from users.models import User


class Profile(models.Model):
    """Profile model.
    We use one to one model that extends the base data with
    other information
    """

    GENDERS = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say')
    ]

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    website = models.URLField(max_length=200, blank=True)
    biography = models.TextField(blank=True)

    picture = models.ImageField(upload_to='users/pictures', blank=True, null=True)
    gender = models.CharField(max_length=2, choices=GENDERS, default='P')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return username"""
        return self.user.username


class Following(models.Model):
    """ Following model
    have all the profiles that a person follow
    """

    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE, related_name='profile_id')
    following = models.ForeignKey('users.Profile', on_delete=models.CASCADE, related_name='following')