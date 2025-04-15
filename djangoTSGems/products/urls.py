from django.urls import path 

from djangoTSGems.products.views import product_view

urlpatterns = [
    path('products', product_view, name='products')
]