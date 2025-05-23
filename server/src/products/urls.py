from django.urls import path
from src.products.views import ProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='products-list'),
    # path('categories/', CategoryListView.as_view(), name='categories-list')
]
