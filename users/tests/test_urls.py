"""Django urls tests"""
# Django
from django.test import SimpleTestCase
from django.urls import resolve, reverse
# Views
from users.views import (
    LoginView,
    LogoutView,
    SignUpView,
    UpdateProfile,
    UserDetailView
)


class TestUserUrls(SimpleTestCase):
    """Test all user's Urls """

    def test_login_url_resolves(self):
        """login url"""
        url = reverse('users:login')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_logout_url_resolves(self):
        """logout url"""
        url = reverse('users:logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_signup_url_resolves(self):
        """signup url"""
        url = reverse('users:signup')
        self.assertEquals(resolve(url).func.view_class, SignUpView)

    def test_update_url_resolves(self):
        """update url"""
        url = reverse('users:update')
        self.assertEquals(resolve(url).func.view_class, UpdateProfile)

    def test_detail_url_resolves(self):
        """detail url"""
        url = reverse('users:detail', args=['an_username'])
        self.assertEquals(resolve(url).func.view_class, UserDetailView)