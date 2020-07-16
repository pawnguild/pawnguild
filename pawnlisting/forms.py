from django.forms import ModelForm
from .models import UserProfile
from urllib.parse import urlparse


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["steam_url"]

    def clean_steam_profile(self):
        parsed = urlparse(self.cleaned_data["steam_url"])
        if parsed.netloc != "steamcommunity.com":
            raise ValidationError("Steam URL must be a steamcommunity.com link")
        return self.cleaned_data["steam_url"]
