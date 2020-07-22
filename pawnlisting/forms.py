from django import forms
from .models import UserProfile, SteamPawn, SwitchPawn, XboxOnePawn
from urllib.parse import urlparse
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .utility import base_pawn_fields, steam_pawn_fields, switch_pawn_fields


class UserProfileForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = UserCreationForm.Meta.fields


class SteamPawnForm(forms.ModelForm):
    
    class Meta:
        model = SteamPawn
        fields = steam_pawn_fields
    
    def clean_steam_url(self):
        parsed = urlparse(self.cleaned_data["steam_url"])
        if parsed.netloc != "steamcommunity.com":
            raise ValidationError("Steam URL must be a steamcommunity.com link")
        return self.cleaned_data["steam_url"]


class SwitchPawnForm(forms.ModelForm):

    class Meta:
        model = SwitchPawn
        fields = switch_pawn_fields
    
class XboxOnePawnForm(forms.ModelForm):

    class Meta:
        model = XboxOnePawn
        fields = base_pawn_fields