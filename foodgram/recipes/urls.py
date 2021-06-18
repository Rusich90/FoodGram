from django.urls import path
from .views import (IndexView, SubscriptionsView, FavoriteView, favorite_add,
                    favorite_remove, AuthorView, RecipeView, subscription_add,
                    subscription_remove, purchase_add, purchase_remove,
                    PurchasesView, shop_list, new_recipe, ingredients_search)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('new/', new_recipe, name='new_recipe'),
    path('ingredients', ingredients_search, name='ingredients_search'),
    path('subscriptions/', SubscriptionsView.as_view(), name='follow_index'),
    path('my-follow/', FavoriteView.as_view(), name='favorite_recipes'),
    path('favorites/<int:recipe_id>', favorite_remove, name='removeFavorite'),
    path('favorites', favorite_add, name='addFavorite'),
    path('purchases/', PurchasesView.as_view(), name='purchases'),
    path('recipe/<str:pk>/', RecipeView.as_view(), name='recipe-detail'),
    path('subscriptions/<int:author_id>', subscription_remove, name='removeSubscriptions'),
    path('subscriptions', subscription_add, name='addSubscriptions'),
    path('purchases', purchase_add, name='addPurchases'),
    path('purchases/<int:recipe_id>', purchase_remove, name='removePurchases'),
    path('shoplist/', shop_list, name='shop_list'),

    path('<str:username>/', AuthorView.as_view(), name='profile'),
]
