from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import (UserCreationForm,
                                       AuthenticationForm,
                                       PasswordResetForm,
                                       SetPasswordForm
                                       )


# class UserLoginForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super(UserLoginForm, self).__init__(*args, **kwargs)
#
#     username = forms.CharField(widget=forms.TextInput(attrs={
#         "class": "input",
#         "type": "text",
#         "placeholder": "enter username"
#     }))
#
#     password = forms.CharField(widget=forms.TextInput(attrs={
#         "class": "input",
#         "type": "password",
#         "placeholder": "enter password"
#     }))


class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "email",
        "placeholder": "enter email-id"
    }))


class NewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': "input",
            "type": "password",
            'autocomplete': 'new-password'
        }))

    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': "input",
            "type": "password",
            'autocomplete': 'new-password'
        }))


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placeholder": "enter username"
    }))

    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "email",
        "placeholder": "enter email-id"
    }))

    address = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placeholder": "enter location"
    }))

    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "phone",
        "placeholder": "enter mobile"
    }))

    password1 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "password",
        "placeholder": "enter password"
    }))

    password2 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "password",
        "placeholder": "re-enter password"
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'address', 'phone_number', 'password1', 'password2']





#
# class UserRegisterFrom(UserCreationForm):
#     email = forms.EmailField()
#     address = forms.Textarea()
#     phone_number = forms.IntegerField()
#
#     class Meta:
#        model = User
#        fields = ['username', 'email','address','phone_number','password1', 'password2']
#
#
#
