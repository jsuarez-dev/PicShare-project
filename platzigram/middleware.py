""" Platzigram middleware catalog."""
# Django
from django.shortcuts import redirect
from django.urls import reverse


class ProfileCompletionMiddleware:
    """Profile completion middleware:
    This middleware ensure that every user has his/her profile full fill.
    """

    def __init__(self, get_response):
        """ Middleware initialization. """
        self.get_response = get_response

    def __call__(self, request):
        """ Code to be executed for each request before the view is called."""

        if not request.user.is_anonymous:
            if not request.user.is_staff:
                profile = request.user.profile
                if not profile.picture or not profile.biography:
                    if request.path not in [reverse('users:update'), reverse('users:logout')]:
                        return redirect('users:update')

        response = self.get_response(request)
        return response
