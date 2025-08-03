from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView


from src.accounts.views import (
    PhotoUploadView,
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    UserDeleteView,
    UserProfileView,
    PasswordChangeView,
)


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path(
        'reset-password-request/',
        PasswordResetRequestView.as_view(),
        name='reset-password-request',
    ),
    path(
        'reset-password-confirm/',
        PasswordResetConfirmView.as_view(),
        name='reset-password-confirm',
    ),
    path('delete/', UserDeleteView.as_view(), name='delete'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('photo/', PhotoUploadView.as_view(), name='photo'),
    path(
        'change-password/',
        PasswordChangeView.as_view(),
        name='change-password',
    ),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
]
