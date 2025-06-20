from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.shortcuts import redirect

urlpatterns = [
    # path('admin/', lambda request: redirect(reverse_lazy('admin:products_product_changelist'))),
    path('admin/', admin.site.urls),
    path('products/', include('src.products.urls'))
]
