from django import forms
from .models import SteamPawn, SwitchPawn, XboxOnePawn, PS4Pawn, PS3Pawn, build_choices
from urllib.parse import urlparse
from django.core.exceptions import ValidationError
from .utility import (
    base_pawn_fields,
    steam_pawn_fields,
    switch_pawn_fields,
    xbox1_pawn_fields,
    ps3_pawn_fields,
    ps4_pawn_fields,
    platforms,
)


class PlatformForm(forms.Form):
    platform = forms.ChoiceField(choices=build_choices(platforms), required=True)


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
        fields = xbox1_pawn_fields


class PS4PawnForm(forms.ModelForm):
    class Meta:
        model = PS4Pawn
        fields = ps4_pawn_fields


class PS3PawnForm(forms.ModelForm):
    class Meta:
        model = PS3Pawn
        fields = ps3_pawn_fields
