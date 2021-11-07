"""User Views"""

# Django
from django.views.generic import DetailView, UpdateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
# Models
from aigram.users.models import User
from aigram.posts.models import Post
from aigram.users.models import Profile


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
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username': username})
