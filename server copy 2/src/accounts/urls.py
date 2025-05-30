from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from src.accounts.views import (
    PhotoUploadView,
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    UserDeleteView,
    UserDetailView
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('delete/', UserDeleteView.as_view(), name='delete'),
    path('detail/', UserDetailView.as_view(), name='detail'),
    path('photo/', PhotoUploadView.as_view(), name='photo'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
]
