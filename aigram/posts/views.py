"""Post Views"""
# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.fields import SlugField
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.urls import reverse_lazy
# Forms
from aigram.posts.forms import PostForm

# Models
from aigram.posts.models import Post
from aigram.posts.models import Comment


class PostDetailView(LoginRequiredMixin, DetailView):
    """ Return detail of a specific post."""

    template_name = 'posts/detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id_post'
    queryset = Post.objects.all()
    context_object_name = 'post'


class PostsCommentsView(LoginRequiredMixin, CreateView):
    """ Receive comment, non return any """
    template_name = 'posts/feed.html'
    model = Comment
    fields = ['message']
    success_url = reverse_lazy('posts:feed')


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
