from django import template
from ..models import Subscription, Favorite, Purchase

register = template.Library()


@register.filter
def is_subscribe(author, user):
    return Subscription.objects.filter(user=user, author=author).exists()


@register.filter
def is_favorite(recipe, user):
    return Favorite.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def is_purchase(recipe, user):
    return Purchase.objects.filter(user=user, recipe=recipe).exists()
