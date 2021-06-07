from django.urls import path
from .views import IndexView, SubscriptionsView, FavoriteView, favorite_add, favorite_remove, AuthorView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('subscriptions/', SubscriptionsView.as_view(), name='follow_index'),
    path('my-follow/', FavoriteView.as_view(), name='favorite_recipes'),
    path('favorites/<int:recipe_id>', favorite_remove, name='removeFavorite'),
    path('favorites', favorite_add, name='addFavorite'),
    path('<str:username>/', AuthorView.as_view(), name='profile'),
]
