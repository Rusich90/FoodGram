from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Recipe, User, Favorite
from .models import Tag


class IndexView(ListView):
    model = Recipe
    template_name = 'index.html'
    paginate_by = 6

    def get_queryset(self):
        tag = self.kwargs.get('tag', )
        object_list = self.model.objects.all()
        if tag:
            object_list = object_list.filter(title__icontains=tag)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        if self.request.user.is_authenticated:
            context['favorite_recipes'] = Recipe.objects.filter(
                favorites__user=self.request.user)
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

