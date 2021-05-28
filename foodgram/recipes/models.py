from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=16)
    color = models.CharField(max_length=16)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(max_length=128)
    dimension = models.CharField(max_length=16)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.ingredient.title


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField()
    ingredients = models.ManyToManyField(RecipeIngredient)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)
    cooking_time = models.PositiveIntegerField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение',
        help_text='Загрузите изображение (необязательно)',
        blank=True,
        null=True)

    def __str__(self):
        return self.title
