from django import template

register = template.Library()


@register.filter
def is_owner(obj, user):
    return obj.owner == user
