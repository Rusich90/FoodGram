from django.shortcuts import render
from django.views.generic import ListView
from .models import Recipe


class IndexView(ListView):
    model = Recipe
    template_name = 'signup.html'
    paginate_by = 6