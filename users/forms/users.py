""" User Forms """
# Django
from django import forms
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
# Models
from users.models import User
from users.models import Profile
# Utilities
from datetime import timedelta
import jwt


class SignupForm(forms.Form):
    """ Signup form """

    username = forms.CharField(min_length=4, max_length=50)

    password = forms.CharField(
        min_length=4,
        max_length=70,
        widget=forms.PasswordInput()
    )
    password_confirmation = forms.CharField(
        min_length=4,
        max_length=70,
        widget=forms.PasswordInput()
    )

    first_name = forms.CharField(min_length=2, max_length=50)
    last_name = forms.CharField(min_length=2, max_length=50)

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput()
    )

    def clean_username(self):
        """ Username must be unique. """
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('Username is already use')
        return username

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()
        if not data.get('password') and not data.get('password_confirmation'):
            raise forms.ValidationError('Password or Password confirmation was not provided')
        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match')
        return data

    def save(self):
        """ Create user and profile"""
        user = self.cleaned_data
        user.pop('password_confirmation')

        user = User.objects.create_user(**user)

        profile = Profile(user=user)
        profile.save()
        self.send_validation_email(user=user)

    def send_validation_email(self, user):
        """send email validation"""
        verification_token = self.generate_verification_token(user)
        subject = 'Welcome @{}! Verify your account to start using AIgram'.format(user.username)
        from_email = 'AI-gram <noreply@aigram.com>'
        content = render_to_string(
            'emails/users/account_verification.html',
            {
                'token': verification_token,
                'user': user,
                'SITE_URL': settings.SITE_URL
            }
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, 'text/html')
        msg.send()

    def generate_verification_token(self, user):
        """ Create JWT token that he user can use to verify its account """
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return token.decode()
