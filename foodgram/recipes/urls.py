from django.urls import path
from .views import IndexView, SubscriptionsView, FavoriteView, favorite_add, favorite_remove, AuthorView, RecipeView, subscription_add, subscription_remove


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('subscriptions/', SubscriptionsView.as_view(), name='follow_index'),
    path('my-follow/', FavoriteView.as_view(), name='favorite_recipes'),
    path('favorites/<int:recipe_id>', favorite_remove, name='removeFavorite'),
    path('favorites', favorite_add, name='addFavorite'),
    path('<str:username>/', AuthorView.as_view(), name='profile'),
    path('recipe/<str:pk>/', RecipeView.as_view(), name='recipe-detail'),
    path('subscriptions/<int:author_id>', subscription_remove, name='removeSubscriptions'),
    path('subscriptions', subscription_add, name='addSubscriptions'),
]
