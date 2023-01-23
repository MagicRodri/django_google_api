import bleach
from django import template

register = template.Library()


@register.filter
def replace_url_with_link(text: str) -> str:
    """
    Replace URLs in text with HTML links
    """
    return bleach.linkify(bleach.clean(text))