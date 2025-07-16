from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/accounts/', include('src.accounts.urls')),

    path('api/products/', include('src.products.urls')),

    path('api/shopping-bags/', include('src.shopping_bags.urls')),

    path('api/orders/', include('src.orders.urls')),

    path('api/wishlist/', include('src.wishlists.urls')),
]
