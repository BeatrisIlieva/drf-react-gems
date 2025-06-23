from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('src.products.urls')),
    path('shopping-bags/', include('src.shopping_bags.urls')),
]
