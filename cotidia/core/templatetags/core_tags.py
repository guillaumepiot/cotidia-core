from django import template

from cotidia.core.utils.static import absolute_url as make_absolute_url

register = template.Library()


@register.filter
def absolute_url(value):
    return make_absolute_url(value)


@register.simple_tag
def status_list_for_obj(obj, taxonomy=None, user=None):
    return obj.status_list(taxonomy=taxonomy, user=user)
