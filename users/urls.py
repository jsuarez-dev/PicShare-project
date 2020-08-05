"""Users' URLs"""

# Django
from django.urls import path

# Local
from users import views

urlpatterns = [

    # Management
    path(
        route='login/',
        view=views.LoginView.as_view(),
        name='login'
    ),

    path(
        route='logout/',
        view=views.LogoutView.as_view(),
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
    path(
        route='email/verify/',
        view=views.VerifyEmailView.as_view(),
        name='verify'
    ),
    path(
        route='email/confirm_sent/',
        view=views.ConfirmEmailVerificationSentView.as_view(),
        name='email_confirm_sent'
    ),
    path(
        route='email/no_verified/',
        view=views.ConfirmEmailVerificationSentView.as_view(),
        name='email_no_verified'
    )
    ,
    path(
        route='email/send/',
        view=views.SendEmailVerificationView.as_view(),
        name='send_email_verification'
    )
]
