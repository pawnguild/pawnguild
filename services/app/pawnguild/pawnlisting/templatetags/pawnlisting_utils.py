from django import template
from django.core.exceptions import ValidationError

from ..validators import validate_steam_url

register = template.Library()


@register.filter
def steam_profile_url(value):
    # Old listings may contain links that predate form validation.
    try:
        validate_steam_url(value)
    except (ValidationError, ValueError, TypeError):
        return ""
    return value


@register.filter("startswith")
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter("add_is_active")
def add_is_active(requestPath, args):
    classText, uri = args.split(",")
    # breakpoint()
    if requestPath.startswith(uri):
        return classText + " active"
    return classText


@register.simple_tag(takes_context=True)
def pawn_page_query(context, parameter, page):
    query = context["request"].GET.copy()
    query[parameter] = page
    return query.urlencode()
