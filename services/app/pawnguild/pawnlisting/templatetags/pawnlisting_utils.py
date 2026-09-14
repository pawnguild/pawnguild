from django import template

register = template.Library()


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
