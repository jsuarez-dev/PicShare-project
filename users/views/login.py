"""User Views"""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import reverse


class LoginView(auth_views.LoginView):
    """Login View."""

    template_name = 'users/login.html'

    def form_valid(self, form):
        """check if the user is verified"""

        if not form.get_user().is_verified:
            return redirect('users:email_no_verified')
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = 'users/logout.html'