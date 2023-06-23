from django import template

register = template.Library()

@register.filter(name="zip")
def zipf(list1, list2):
    return zip(list1, list2)

@register.filter(name="subtract")
def subtract(value, args):
    return value - args


