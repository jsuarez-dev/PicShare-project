# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend, BaseBackend
# Models
from users.models import User


class EmailModelBackend(ModelBackend):
    """
    This is a ModelBacked that allows authentication with either a username or an email address.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):

        if '@' in username:
            kwargs = {'email': username}
        else:
            return None
        if password is None:
            return None
        try:
            user = User.objects.get(**kwargs)

        except User.DoesNotExist:
            User.set_password(password)

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None