from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reportlab
from django.conf import settings
import io
from django.http import FileResponse
from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from .models import Ingredient, RecipeIngredient


def create_pdf(purchases_dict):
    buffer = io.BytesIO()
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
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Список покупок.pdf')


def get_ingredients(request):
    ingredients = {}
    for key, title in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[title] = request.POST[
                f'valueIngredient_{num}'
            ]
    return ingredients


def save_recipe(request, form):
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            objs = []
            ingredients = get_ingredients(request)
            for title, amount in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=title)
                objs.append(
                    RecipeIngredient(
                        recipe=recipe,
                        ingredient=ingredient,
                        amount=amount
                    )
                )
            RecipeIngredient.objects.bulk_create(objs)
            form.save_m2m()
            return recipe

    except IntegrityError:
        raise HttpResponseBadRequest
