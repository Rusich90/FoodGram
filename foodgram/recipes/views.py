from django.shortcuts import render
from django.views.generic import ListView
from .models import Recipe
from .models import Tag
from urllib.parse import unquote


class IndexView(ListView):
    model = Recipe
    template_name = 'index.html'
    paginate_by = 6

    def get_queryset(self):
        print(self.kwargs.get('tag', ))
        tag = self.kwargs.get('tag', )
        object_list = self.model.objects.all()
        if tag:
            object_list = object_list.filter(title__icontains=tag)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        return context
