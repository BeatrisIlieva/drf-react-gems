from django.urls import path

from src.products.views import CategoryListView, ProductItemListView

urlpatterns = [
    path('', ProductItemListView.as_view(), name='products'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
]
