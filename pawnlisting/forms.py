from django import forms
from .models import UserProfile, SteamPawnProfile, SwitchPawnProfile
from urllib.parse import urlparse


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = []


class SteamPawnProfileForm(forms.ModelForm):
    
    class Meta:
        model = SteamPawnProfile
        fields = ["steam_url"]
    
    def clean_steam_profile(self):
        parsed = urlparse(self.cleaned_data["steam_url"])
        if parsed.netloc != "steamcommunity.com":
            raise ValidationError("Steam URL must be a steamcommunity.com link")
        return self.cleaned_data["steam_url"]

class SwitchPawnProfileForm(forms.ModelForm):

    class Meta:
        model = SwitchPawnProfile
        fields = ["friend_code", "pawn_code"]