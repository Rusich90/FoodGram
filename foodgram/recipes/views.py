from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Recipe, User, Favorite, Subscription
from .models import Tag


class IndexView(ListView):
    template_name = 'index.html'
    paginate_by = 6

    def get_queryset(self):
        tag = self.kwargs.get('tag', )
        object_list = Recipe.objects.all()
        if tag:
            object_list = object_list.filter(title__icontains=tag)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            context['tag_list'] = Tag.objects.all()
            context['subscription_list'] = Subscription.objects.filter(
                user=user)
            context['favorite_recipes'] = Recipe.objects.filter(
                favorites__user=user)
        return context


class AuthorView(IndexView):
    template_name = 'authorRecipe.html'

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs['username'])
        tag = self.kwargs.get('tag', )
        object_list = Recipe.objects.filter(author=author)
        if tag:
            object_list = object_list.filter(title__icontains=tag)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs['username'])
        context['author'] = author
        return context


class SubscriptionsView(ListView):
    template_name = 'myFollow.html'
    paginate_by = 6

    def get_queryset(self):
        object_list = User.objects.filter(
            following__user=self.request.user)
        return object_list


class FavoriteView(ListView):
    template_name = 'favorite.html'
    paginate_by = 6

    def get_queryset(self):
        object_list = Recipe.objects.filter(
            favorites__user=self.request.user)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        context['favorite_recipes'] = Recipe.objects.filter(
            favorites__user=self.request.user)
        return context


@login_required
def favorite_add(request):
    recipe_id = json.loads(request.body).get("id")
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    favorite_recipe = Favorite.objects.create(user=user, recipe=recipe)
    favorite_recipe.save
    return JsonResponse({"success": True})


@login_required
def favorite_remove(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    favorite_recipe = Favorite.objects.get(user=user, recipe=recipe)
    favorite_recipe.delete()
    return JsonResponse({"success": True})

