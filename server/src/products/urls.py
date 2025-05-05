from django.urls import path

from src.products.views import CategoryListView, ProductItemByCategoryView

urlpatterns = [
    # path('', ProductItemListView.as_view(), name='products'),
     path('<int:category_id>/', ProductItemByCategoryView.as_view(), name='product-by-category'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
]
