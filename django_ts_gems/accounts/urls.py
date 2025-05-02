from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from django_ts_gems.accounts.views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
]
