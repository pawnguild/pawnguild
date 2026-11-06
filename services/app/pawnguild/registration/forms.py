from .models import UserProfile
from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.db.models import Q


class PasswordRecoveryForm(PasswordResetForm):
    email = None
    username_or_email = forms.CharField(label="Username or email", max_length=254)

    def get_users(self, username_or_email):
        users = get_user_model().objects.filter(
            Q(username=username_or_email) | Q(email__iexact=username_or_email),
            is_active=True,
        )
        return (user for user in users if user.has_usable_password())

    def save(self, **kwargs):
        self.cleaned_data["email"] = self.cleaned_data["username_or_email"]
        return super().save(**kwargs)


class UserProfileCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = UserCreationForm.Meta.fields + ("email",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError("Username is already in use")
        return username
