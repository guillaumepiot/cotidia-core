from django import template

from cotidia.core.utils.static import absolute_url as make_absolute_url

register = template.Library()


@register.filter
def absolute_url(value):
    return make_absolute_url(value)
