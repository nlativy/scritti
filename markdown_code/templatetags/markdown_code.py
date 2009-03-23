from django import template
from django.template.defaultfilters import stringfilter
from scritti.utils import markdown_pygment

register = template.Library()

@register.filter
@stringfilter
def markdown_code(txt):
    return markdown_pygment(txt)
