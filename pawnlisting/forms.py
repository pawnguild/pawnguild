from django import forms
from .models import Pawn, UserProfile, SteamPawn, SwitchPawn
from urllib.parse import urlparse
from django.core.exceptions import ValidationError

from .utility import steam_pawn_fields, switch_pawn_fields


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = []


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
    