"""Post Views"""
# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
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
    """Return all published posts."""

    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 2
    context_object_name = 'posts'


@login_required
def create_post(request):
    """Function to create new a post view."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:feed')

    else:
        form = PostForm()

    return render(
        request=request,
        template_name='posts/new.html',
        context={
            'form': form,
            'user': request.user,
            'profile': request.user.profile,
        }
    )
