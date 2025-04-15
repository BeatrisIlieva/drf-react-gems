from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('djangoTSGems.accounts.urls')),
    path('', include('djangoTSGems.products.urls'))
]
