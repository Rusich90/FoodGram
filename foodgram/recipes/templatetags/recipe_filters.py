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


@register.filter
def get_filter_values(get_params):
    return get_params.getlist("tags")


@register.filter
def get_filter_link(get_params, tag):
    tags: list = get_params.getlist("tags")
    if tag.name in tags:
        tags.remove(tag.name)
    else:
        tags.append(tag.name)

    if tags:
        result = "tags=" + "&tags=".join(tags)
        return result


@register.filter
def get_tags(get_params):
    tags = get_params.getlist("tags")
    if tags:
        result = "tags=" + "&tags=".join(tags)
        return result
