from django.contrib.auth.views import LogoutView
from django.urls import path
import django_ts_gems.accounts.views as views

urlpatterns = [
    path('register/', views.AppUserRegisterView.as_view(), name='register'),
    path('login/', views.AppUserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', views.index, name='home')
    # path('home/', views.HomeView.as_view(), name='home')

    # path('account/<int:pk>/', include([
    #     path('', views.account_)
    # ]))
]
