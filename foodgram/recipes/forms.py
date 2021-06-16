from .models import Recipe
from django import forms


class RecipeForm(forms.ModelForm):
    title = forms.CharField(max_length=256)
    cooking_time = forms.IntegerField(min_value=1)

    class Meta:
        model = Recipe
        fields = ('title', 'tag', 'cooking_time', 'description', 'image')
        widgets = {'tags': forms.CheckboxSelectMultiple()}