"""platzigram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# django
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

# local
from platzigram import views as local_views
from posts import views as post_views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', local_views.hello_world, name='hello'),
    path('sorted/', local_views.sorted_numbers, name='sort'),
    path('hi/<str:name>/<int:age>/', local_views.say_hi, name='hi'),
    path('posts/', post_views.list_posts, name='feed'),
    path('users/login', user_views.login_view, name='login'),
    path('users/logout', user_views.logout_view, name='logout'),
    path('users/signup', user_views.signup, name='signup')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
