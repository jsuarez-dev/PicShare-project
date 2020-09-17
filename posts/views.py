"""Post Views"""
# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy
# Forms
from posts.forms import PostForm

# Models
from posts.models import Post


class PostDetailView(LoginRequiredMixin, DetailView):
    """ Return detail of a specific post."""

    template_name = 'posts/detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id_post'
    queryset = Post.objects.all()
    context_object_name = 'post'


class PostsFeedView(LoginRequiredMixin, ListView):
    """ Return all published posts."""

    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 20
    context_object_name = 'posts'


class CreatePostView(LoginRequiredMixin, FormView):
    """Class to create new a post view."""

    template_name = 'posts/new.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:feed')

    def get_form_kwargs(self):
        kwargs = super(CreatePostView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)