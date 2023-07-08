from django import template
from ..models import *

register = template.Library()

@register.filter(name="zip")
def zipf(list1, list2):
    return zip(list1, list2)

@register.filter(name="subtract")
def subtract(value, args):
    return value - args

@register.filter(name="has_perm")
def has_permission(user, perm):
    return user.has_perm(perm)

@register.filter(name="count_followers")
def count_followers(user1):
    return user1.followers.all().count()


