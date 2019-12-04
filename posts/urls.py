"""Post's URLs"""

# Django
from django.urls import path

# Local
from posts import views

urlpatterns = [

    path(
        route='',
        view=views.PostsFeedView.as_view(),
        name='feed'
    ),

    path(
        route='posts/<int:id_post>/',
        view=views.PostDetailView.as_view(),
        name='detail'
    ),

    path(
        route='posts/new/',
        view=views.CreatePostView.as_view(),
        name='create'
    ),
]
