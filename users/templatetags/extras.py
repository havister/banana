from django import template

register = template.Library()

@register.filter
def change_class(value):
    return 'text-red' if value >= 0 else 'text-blue'
