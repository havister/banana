from django import template

register = template.Library()

@register.filter
def position_word(value):
    return 'Long' if value == 'L' else 'Short'

@register.filter
def change_class(value):
    return 'text-red' if value >= 0 else 'text-blue'
