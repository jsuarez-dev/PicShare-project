"""User Views"""

# Django
from django.views.generic import DetailView, FormView, UpdateView, TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.shortcuts import redirect
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

        if not request.user.is_anonymous and request.user.is_authenticated:
            return redirect(reverse('posts:feed'))

        token = request.GET.get('token')
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.InvalidSignatureError:
                context['status'] = 'Invalid Token'
                return self.render_to_response(context)
            except jwt.ExpiredSignature:
                context['status'] = 'Token has expired'
                return self.render_to_response(context)
            except jwt.PyJWTError:
                context['status'] = 'Invalid Token'
                return self.render_to_response(context)

            if payload['type'] != 'email_confirmation':
                context['status'] = 'Invalid Token'
                return self.render_to_response(context)

            # Query user
            try:
                user = User.objects.get(username=payload['user'])
            except User.DoesNotExist:
                return redirect(reverse('users:login'))

            if user.is_verified:
                return redirect(reverse('users:login'))

            user.is_verified = True
            user.save()
            context['status'] = 'successful'
        else:
            return redirect(reverse('users:login'))
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
