"""Posts model."""

# Django
from django.contrib import admin

# Models
from aigram.posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post admin."""

    list_display = ('id', 'user', 'caption', 'photo')
    search_fields = ('caption', 'user__username', 'user__email')
    list_filter = ('created', 'modified')
