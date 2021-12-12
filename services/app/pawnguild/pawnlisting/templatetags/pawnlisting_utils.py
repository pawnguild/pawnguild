from django import template

register = template.Library()

@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter('add_is_active')
def add_is_active(requestPath, args):
    classText, uri = args.split(',')
    # breakpoint()
    if requestPath.startswith(uri):
        return classText + ' active'
    return classText