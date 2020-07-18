"""tags models"""

# Django
from django.db import models


class Tag(models.Model):
    """Tag model"""
    name = models.CharField(max_length=50)

    def __str__(self):
        """:return tag name"""
        return '{}'.format(self.name)

