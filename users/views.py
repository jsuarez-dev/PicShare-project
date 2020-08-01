"""User Views"""

# Django
from django.views.generic import DetailView, FormView, UpdateView, TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.conf import settings
# Models
from users.models import User
from posts.models import Post
from users.models import Profile
# Forms
from users.forms import SignupForm
# Utilities
import jwt


class SendEmailVerificationView(TemplateView):
    template_name = 'users/send_email_verification.html'


class VerifyEmailView(TemplateView):
    """Verify email"""

    template_name = 'users/email_verified.html'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        """Verify the JWT token"""
        context = self.get_context_data(**kwargs)
        token = request.GET['token']
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignature:
                raise auth_views.ValidationError('Verification link has expired.')
            except jwt.PyJWTError:
                raise auth_views.ValidationError('Invalid token')

            if payload['type'] != 'email_confirmation':
                raise auth_views.ValidationError('Invalid token')

            user = User.objects.get(username=payload['user'])
            user.is_verified = True
            user.save()
        else:
            raise auth_views.ValidationError('no token')
        return self.render_to_response(context)


class UserDetailView(LoginRequiredMixin, DetailView):
    """User detail view"""
    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """add user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context


class UpdateProfile(LoginRequiredMixin, UpdateView):
    """Update profile View"""
    template_name = 'users/update_profile.html'
    model = Profile
    fields = ['website', 'biography', 'picture']

    def get_object(self):
        """Return user's profile"""
        return self.request.user.profile

    def get_success_url(self):
        """Return to user's profile."""
        username = self.object.user.usernamet
        return reverse('users:detail', kwargs={'username': username})


class LoginView(auth_views.LoginView):
    """Login View."""

    template_name = 'users/login.html'


class SignUpView(FormView):
    """Class Sign up view"""
    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:send_email_verification')

    def form_valid(self, form):
        """ Save the form. """
        form.save()
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = 'users/logout.html'
