"""comments models"""

# Django
from django.db import models


class Comment(models.Model):
    """Comment Model"""
    message = models.CharField(max_length=500)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)

    def __str__(self):
        """:return post title and who made the comment"""
        return "Comment in {} by @{}".format(self.post.title, self.profile.user.username)