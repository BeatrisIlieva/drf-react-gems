from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    path('',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('admin/', admin.site.urls),
    path('api/accounts/', include('src.accounts.urls')),
    path('api/products/', include('src.products.urls')),
    path('api/shopping-bags/', include('src.shopping_bags.urls')),
    path('api/orders/', include('src.orders.urls')),
    path('api/wishlist/', include('src.wishlists.urls')),
    # Reviews are handled within the products app
]
