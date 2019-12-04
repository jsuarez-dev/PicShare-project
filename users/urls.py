"""Users' URLs"""

# Django
from django.urls import path

# Local
from users import views

urlpatterns = [

    # Management
    path(
        route='login/',
        view=views.login_view,
        name='login'
    ),

    path(
        route='logout/',
        view=views.logout_view,
        name='logout'
    ),

    path(
        route='signup/',
        view=views.SignUpView.as_view(),
        name='signup'
    ),

    path(
        route='me/profile/',
        view=views.UpdateProfile.as_view(),
        name='update'
    ),
    # Post
    path(
        route='<str:username>/',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
]
