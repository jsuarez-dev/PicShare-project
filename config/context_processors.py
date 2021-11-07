"""Add extra context to the templates"""
from django.conf import settings


def site_url(request):
    """
    Site url
    """
    return {'SITE_URL': settings.SITE_URL}

