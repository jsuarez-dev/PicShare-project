""" Models likes """
# Django
from django.db import models
# Models


class Like(models.Model):
    """
    Likes model has the next fields:
    user
    """
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
