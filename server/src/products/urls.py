from django.urls import path
from src.products.views import ProductListAPIView

urlpatterns = [
    path('', ProductListAPIView.as_view(), name='product-list'),
]
