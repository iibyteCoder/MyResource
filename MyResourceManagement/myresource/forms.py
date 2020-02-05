from django import forms
from django.core.exceptions import ValidationError


def nameValidator(name):
    pool = ['***']
    for i in pool:
        if i in str(name):
            raise ValidationError


class RegistryValid(forms.Form):
    username = forms.CharField(max_length=16, validators=(nameValidator,))
    password = forms.CharField(max_length=32, )
    email = forms.EmailField()
