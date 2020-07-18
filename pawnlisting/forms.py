from django import forms
from .models import Pawn, UserProfile, SteamPawnProfile, SwitchPawnProfile
from urllib.parse import urlparse
from django.core.exceptions import ValidationError

class PawnForm(forms.ModelForm):

    class Meta:
        model = Pawn
        fields = ["name", "level", "vocation", "gender", "primary_inclination",
    "secondary_inclination", "tertiary_inclination", "notes", "picture", "platform"]

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = []


class SteamPawnProfileForm(forms.ModelForm):
    
    class Meta:
        model = SteamPawnProfile
        fields = ["steam_url"]
    
    def clean_steam_url(self):
        parsed = urlparse(self.cleaned_data["steam_url"])
        if parsed.netloc != "steamcommunity.com":
            raise ValidationError("Steam URL must be a steamcommunity.com link")
        return self.cleaned_data["steam_url"]

class SwitchPawnProfileForm(forms.ModelForm):

    class Meta:
        model = SwitchPawnProfile
        fields = ["friend_code", "pawn_code"]