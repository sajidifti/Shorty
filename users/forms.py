from typing import Any
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    SetPasswordForm,
)
from django.contrib.auth import get_user_model
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import SetPasswordForm as BaseSetPasswordForm
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django.utils.translation import gettext_lazy as _


class UserSignUpForm(UserCreationForm):
    """
    Custom User Sign Up Form
    """

    username = forms.CharField(
        max_length=150,
        help_text="Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only.",
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )

    email = forms.EmailField(
        help_text="Required. Add a valid email address.",
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
    )

    first_name = forms.CharField(
        max_length=30,
        help_text="Your first name.",
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
    )

    last_name = forms.CharField(
        max_length=30,
        help_text="Your last name.",
        widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
    )

    password1 = forms.CharField(
        help_text="Enter a password. It should not be too similar to your other personal information or a commonly used password.",
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )

    password2 = forms.CharField(
        help_text="Enter the same password as before, for verification.",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super(UserSignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


class UserLoginForm(AuthenticationForm):
    """
    Custom User Login Form
    """

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username or Email"}
        ),
        label="Username or Email",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class UserUpdateForm(forms.ModelForm):
    """
    Custom User Update Form
    """

    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name", "image"]


# class SetPasswordForm(SetPasswordForm):
#     """
#     Custom Set Password Form
#     """
#     class Meta:
#         model = get_user_model()
#         fields = ["new_password1", "new_password2"]


class SetPasswordForm(BaseSetPasswordForm):
    """
    Custom Set Password Form
    """

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Enter new password")}
        ),
        label=_("New password"),
        help_text=_(
            "Your password must be at least 8 characters long and contain a mix of letters, digits, and symbols."
        ),
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Confirm new password")}
        ),
        label=_("Confirm new password"),
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = get_user_model()
        fields = ["new_password1", "new_password2"]


class PasswordResetForm(BasePasswordResetForm):
    """
    Custom Password Reset Form
    """

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs["placeholder"] = _("Enter your email")
        self.fields["email"].help_text = _(
            "Enter the email address associated with your account."
        )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        fields = ["email"]
