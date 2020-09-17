"""tags models"""

# Django
from django.db import models


class Hashtag(models.Model):
    """Tag model"""
    name = models.CharField(max_length=50)

    def __str__(self):
        """:return tag name"""
        return '{}'.format(self.name)


class PostProfileTag(models.Model):
    """Person tag model"""
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)

    def __str__(self):
        """:return person tag name and post name"""
        return '@{} is tag in {}'.format(self.profile.user.username, self.post)
