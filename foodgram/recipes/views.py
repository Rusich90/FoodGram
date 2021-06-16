import io
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Recipe, User, Favorite, Subscription, Purchase, RecipeIngredient
from .models import Tag
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reportlab
from django.conf import settings

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

    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    reportlab.rl_config.TTFSearchPath.append(
        str(settings.BASE_DIR) + '/fonts')
    pdfmetrics.registerFont(TTFont('FreeSans', '../fonts/FreeSans.ttf'))
    p.setFont('FreeSans', 20)
    p.drawString(250, 800, "FoodGram")
    p.drawString(30, 750, "Список покупок:")
    p.setFont('FreeSans', 16)
    x = 710
    for key, value in purchases_dict.items():
        p.drawString(30, x, f" - {key} - {value[0]} {value[1]}")
        x -= 30
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Список покупок.pdf')
