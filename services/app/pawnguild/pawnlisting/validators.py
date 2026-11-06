from urllib.parse import urlparse

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def validate_steam_url(value):
    URLValidator(schemes=["http", "https"])(value)
    if urlparse(value).netloc != "steamcommunity.com":
        raise ValidationError("Steam URL must be a steamcommunity.com link")
