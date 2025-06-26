from django.urls import path

from src.wishlist.views import (
    WishlistListView,
    WishlistCreateView,
    WishlistDeleteView,
    WishlistCountView,
)

urlpatterns = [
    path('', WishlistListView.as_view(), name='wishlist-list'),
    path('add/', WishlistCreateView.as_view(), name='wishlist-add'),
    path('remove/<str:content_type>/<int:object_id>/', WishlistDeleteView.as_view(), name='wishlist-remove'),
    path('count/', WishlistCountView.as_view(), name='wishlist-count'),
]