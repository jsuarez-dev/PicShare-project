"""Post models."""

# Django
from django.db import models
# Utilities


class Post(models.Model):
    """Post model."""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)

    caption = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='posts/photos')

    tags = models.ManyToManyField('posts.Hashtag')
    location = models.ForeignKey('posts.Location', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return title and username"""
        return '{} by @{}'.format(self.caption, self.user.username)





