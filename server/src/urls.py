"""
Main URL Configuration for DRF React Gems E-commerce Platform

This file defines the top-level URL patterns for the Django application.
It serves as the entry point for all incoming HTTP requests and routes them
to the appropriate Django applications based on the URL path.

URL Structure:
- /admin/ - Django admin interface
- /api/accounts/ - User authentication and profile management
- /api/products/ - Product catalog and inventory
- /api/shopping-bags/ - Shopping cart functionality
- /api/orders/ - Order processing and management
- /api/wishlist/ - User wishlist management

The 'api/' prefix indicates these are REST API endpoints consumed by the React frontend.
"""

# Django admin imports for the admin interface
from django.contrib import admin
# URL routing imports for defining URL patterns
from django.urls import path, include

# Main URL patterns that Django will match against incoming requests
# Django processes these patterns in order, using the first match
urlpatterns = [
    # Django admin interface - provides a web-based admin panel
    # Accessible at /admin/ for managing database records
    path('admin/', admin.site.urls),
    
    # User authentication and profile management endpoints
    # All URLs starting with /api/accounts/ will be handled by the accounts app
    # This includes login, registration, profile management, etc.
    path('api/accounts/', include('src.accounts.urls')),
    
    # Product catalog and inventory management endpoints
    # All URLs starting with /api/products/ will be handled by the products app
    # This includes product listing, details, categories, etc.
    path('api/products/', include('src.products.urls')),
    
    # Shopping cart functionality endpoints
    # All URLs starting with /api/shopping-bags/ will be handled by the shopping_bags app
    # This includes adding/removing items, cart management, etc.
    path('api/shopping-bags/', include('src.shopping_bags.urls')),
    
    # Order processing and management endpoints
    # All URLs starting with /api/orders/ will be handled by the orders app
    # This includes order creation, history, status updates, etc.
    path('api/orders/', include('src.orders.urls')),
    
    # User wishlist management endpoints
    # All URLs starting with /api/wishlist/ will be handled by the wishlists app
    # This includes adding/removing items from wishlist, etc.
    path('api/wishlist/', include('src.wishlists.urls')),
]
