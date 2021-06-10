from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Recipe, User, Favorite, Subscription
from .models import Tag


class IndexView(ListView):
    template_name = 'index.html'
    paginate_by = 6

    def get_queryset(self):
        object_list = Recipe.objects.all()
        if self.request.GET.get('tag'):
            tag = self.request.GET['tag'].split(',')
            object_list = object_list.filter(tag__name__in=tag).distinct()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        return context


class AuthorView(IndexView):
    template_name = 'authorRecipe.html'

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs['username'])
        object_list = Recipe.objects.filter(author=author)
        if self.request.GET.get('tag'):
            tag = self.request.GET['tag'].split(',')
            object_list = object_list.filter(tag__name__in=tag).distinct()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs['username'])
        context['author'] = author
        return context


class SubscriptionsView(IndexView):
    template_name = 'myFollow.html'

    def get_queryset(self):
        object_list = User.objects.filter(
            following__user=self.request.user)
        return object_list


class FavoriteView(IndexView):
    template_name = 'favorite.html'

    def get_queryset(self):
        object_list = Recipe.objects.filter(
            favorites__user=self.request.user)
        if self.request.GET.get('tag'):
            tag = self.request.GET['tag'].split(',')
            object_list = object_list.filter(tag__name__in=tag).distinct()
        return object_list


class RecipeView(DetailView):
    model = Recipe
    template_name = 'singlePage.html'


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

