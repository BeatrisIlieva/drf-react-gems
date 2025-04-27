from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_ts_gems.accounts.urls')),
    path('', include('django_ts_gems.products.urls'))
]
