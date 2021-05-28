from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


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
    amount = models.PositiveIntegerField(validators=(
                                   MinValueValidator(1),
                                   MaxValueValidator(10000)))

    def __str__(self):
        return self.ingredient.title


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    title = models.CharField(max_length=256)
    description = models.TextField()
    ingredients = models.ManyToManyField(RecipeIngredient)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING,
                            related_name='recipes')
    cooking_time = models.PositiveIntegerField(validators=(
                                   MinValueValidator(1),
                                   MaxValueValidator(2000)))
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    db_index=True)
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение',
        help_text='Загрузите изображение (необязательно)',
        blank=True,
        null=True)

    def __str__(self):
        return self.title
