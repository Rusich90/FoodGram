from django.urls import path
from .views import IndexView, SubscriptionsView, FavoriteView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('subscriptions/', SubscriptionsView.as_view(), name='follow_index'),
    path('favorites/', FavoriteView.as_view(), name='favorite_recipes'),
]
