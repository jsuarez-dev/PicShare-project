"""Platzigram URL Configuration"""
# django
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

# local

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include(('posts.urls', 'posts'), namespace='posts')),

    path('users/', include(('users.urls', 'users'), namespace='users')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
