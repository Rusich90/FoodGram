from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    name = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(max_length=128)
    dimension = models.CharField(max_length=16)

    class Meta:
        ordering = ('title', )
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return f'{self.title}, {self.dimension}'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    title = models.CharField(max_length=256)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient,
                                         related_name='recipes',
                                         through='RecipeIngredient')
    tag = models.ManyToManyField(Tag, related_name='recipes')
    cooking_time = models.PositiveIntegerField(validators=(
                                   MinValueValidator(1),
                                   MaxValueValidator(2000)))
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    db_index=True)
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение',
        help_text='Загрузите изображение')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='recipe_ingredients')
    amount = models.PositiveIntegerField(validators=(
                                   MinValueValidator(1),
                                   MaxValueValidator(10000)))

    def __str__(self):
        return self.ingredient.title


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='purchases')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                             related_name='purchases')


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                             related_name='favorites')

    def __str__(self):
        return self.recipe.title


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='following')

    class Meta:
        unique_together = ['user', 'author']
