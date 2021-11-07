"""User Views"""

# Django
from django.views.generic import FormView, TemplateView
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.shortcuts import redirect
# Models
from aigram.users.models import User
# Forms
from aigram.users.forms import SignupForm, SendEmailVerificationForm
# Utilities
import jwt


class SignUpView(FormView):
    """Class Sign up view"""
    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:email_confirm_sent')

    def form_valid(self, form):
        """ Save the form. """
        form.save()
        return super().form_valid(form)


class ConfirmEmailVerificationSentView(TemplateView):
    """Class to confirm the email has been send"""
    template_name = 'users/confirm_email_verification_sent.html'


class EmailNotVerifiedView(TemplateView):
    """Class to show the email hasn't been verified"""
    template_name = 'users/email_not_verified.html'


class SendEmailVerificationView(FormView):
    """Class to resend the email verification"""
    template_name = 'users/send_email_verification.html'
    form_class = SendEmailVerificationForm
    success_url = reverse_lazy('users:email_confirm_sent')

    def form_invalid(self, form):
        """redirect if the email is not verified"""

        error = form.errors.as_data()['email'][0]
        if error.code == 'verified':
            return redirect(reverse('users:login'))
        return super().form_invalid(form)


class VerifyEmailView(TemplateView):
    """Verify email"""

    template_name = 'users/email_verified.html'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        """Verify the JWT token"""
        context = self.get_context_data(**kwargs)

        if not request.user.is_anonymous and request.user.is_authenticated:
            return redirect(reverse('posts:feed'))

        token = request.GET.get('token')
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.InvalidSignatureError:
                return redirect(reverse('users:login'))
            except jwt.ExpiredSignature:
                context['status'] = 'Token has expired'
                return self.render_to_response(context)
            except jwt.PyJWTError:
                return redirect(reverse('users:login'))

            if payload['type'] != 'email_confirmation':
                context['status'] = 'Invalid Token'
                return self.render_to_response(context)

            # Query user
            try:
                user = User.objects.get(username=payload['user'])
            except User.DoesNotExist:
                return redirect(reverse('users:login'))

            if user.is_verified:
                return redirect(reverse('users:login'))

            user.is_verified = True
            user.save()
            context['status'] = 'successful'
        else:
            return redirect(reverse('users:login'))

        return self.render_to_response(context)