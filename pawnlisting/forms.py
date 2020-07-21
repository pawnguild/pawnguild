from django import forms
from .models import Pawn, UserProfile, SteamPawn, SwitchPawn
from urllib.parse import urlparse
from django.core.exceptions import ValidationError

base_pawn_fields = ["name", "level", "vocation", "gender", "primary_inclination",
    "secondary_inclination", "tertiary_inclination", "notes", "picture"]


# class PawnForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["platform"].widget.attrs.update({"onchange": "this.form.submit()"})

#     class Meta:
#         model = Pawn
#         fields = ["name", "level", "vocation", "gender", "primary_inclination",
#     "secondary_inclination", "tertiary_inclination", "notes", "picture", "platform"]

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = []


class SteamPawnForm(forms.ModelForm):
    
    class Meta:
        model = SteamPawn
        fields = base_pawn_fields + ["steam_url"]
    
    def clean_steam_url(self):
        parsed = urlparse(self.cleaned_data["steam_url"])
        if parsed.netloc != "steamcommunity.com":
            raise ValidationError("Steam URL must be a steamcommunity.com link")
        return self.cleaned_data["steam_url"]


class SwitchPawnForm(forms.ModelForm):

    class Meta:
        model = SwitchPawn
        fields = base_pawn_fields + ["friend_code", "pawn_code"]
    