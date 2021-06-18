from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView
from .models import (Recipe, User, Favorite, Subscription,
                     Purchase, RecipeIngredient, Ingredient)
from .models import Tag
from .utils import create_pdf, save_recipe
from .forms import RecipeForm


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


class PurchasesView(IndexView):
    template_name = 'shopList.html'

    def get_queryset(self):
        object_list = Recipe.objects.filter(
            purchases__user=self.request.user)
        return object_list


class RecipeView(DetailView):
    model = Recipe
    template_name = 'singlePage.html'


# class NewRecipeView(CreateView):
#     model = Recipe
#     template_name = 'formRecipe.html'
#     form_class = RecipeForm

@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        save_recipe(request, form)
        return redirect("index")
    print(form['tag'])
    return render(request,
                  "formRecipe.html",
                  {"form": form}
                  )


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


@login_required
def subscription_add(request):
    author_id = json.loads(request.body).get("id")
    author = get_object_or_404(User, id=author_id)
    user = request.user
    subscription = Subscription.objects.create(user=user, author=author)
    subscription.save
    return JsonResponse({"success": True})


@login_required
def subscription_remove(request, author_id):
    author = get_object_or_404(User, id=author_id)
    user = request.user
    subscription = Subscription.objects.get(user=user, author=author)
    subscription.delete()
    return JsonResponse({"success": True})


@login_required
def purchase_add(request):
    recipe_id = json.loads(request.body).get("id")
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    purchase = Purchase.objects.create(user=user, recipe=recipe)
    purchase.save
    return JsonResponse({"success": True})


@login_required
def purchase_remove(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    purchase = Purchase.objects.get(user=user, recipe=recipe)
    purchase.delete()
    return JsonResponse({"success": True})


@login_required
def shop_list(request):
    purchases = RecipeIngredient.objects.filter(recipe__purchases__user=request.user)
    purchases_dict = {}
    for recipe in purchases:
        if recipe.ingredient.title in purchases_dict.keys():
            purchases_dict[recipe.ingredient.title][0] = purchases_dict[recipe.ingredient.title][0] + recipe.amount
        else:
            purchases_dict[recipe.ingredient.title] = [recipe.amount, recipe.ingredient.dimension]
    return create_pdf(purchases_dict)


def ingredients_search(request):
    query = request.GET.get('query')
    data = list(Ingredient.objects.filter(title__icontains=query).values('title', 'dimension'))
    return JsonResponse(data, safe=False)
