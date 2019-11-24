""" User Forms """
# Django
from django import forms


class ProfileForm(forms.Form):
    """ Profile form class """

    website = forms.URLField(max_length=200, required=True)
    biography = forms.CharField(max_length=500, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    picture = forms.ImageField()

