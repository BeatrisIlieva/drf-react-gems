from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.shortcuts import redirect

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
    path('accounts/', include('src.accounts.urls')),
    path('admin/', lambda request: redirect(reverse_lazy('admin:products_productitem_changelist'))),
    path('admin/', admin.site.urls),
    path('products/', include('src.products.urls'))
]
