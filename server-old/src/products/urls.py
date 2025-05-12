from django.urls import path

from src.products.views import CategoryListView, ProductByCategoryView

urlpatterns = [
    # path('', ProductListView.as_view(), name='products'),
     path('<int:category_id>/', ProductByCategoryView.as_view(), name='product-by-category'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
]
