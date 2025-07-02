from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from src.accounts.views import (
    PhotoUploadView,
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    UserDeleteView,
    UserProfileView,
    PasswordChangeView
)

from src.accounts.views.user_address import (
    UserAddressView,
    StateListView,
    CityListView,
    ZipCodeListView,
    StreetAddressListView
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('delete/', UserDeleteView.as_view(), name='delete'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('photo/', PhotoUploadView.as_view(), name='photo'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    
    path('address/', UserAddressView.as_view(), name='user-address'),
    path('address/states/', StateListView.as_view(), name='states-list'),
    path('address/cities/', CityListView.as_view(), name='cities-list'),
    path('address/zip-codes/', ZipCodeListView.as_view(), name='zip-codes-list'),
    path('address/street-addresses/', StreetAddressListView.as_view(), name='street-addresses-list'),
]
