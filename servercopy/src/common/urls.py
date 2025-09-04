from django.urls import path

from src.common.views import (
    WakeUpServerView,
    notify_users_they_have_uncompleted_orders,
    ShoppingBagReminderInfoView,
)

urlpatterns = [
    path(
        'admin-page/',
        notify_users_they_have_uncompleted_orders,
        name='admin-page',
    ),
    path(
        'admin-bag-info/',
        ShoppingBagReminderInfoView.as_view(),
        name='admin-bag-info',
    ),
    path(
        'wake-up-server/',
        WakeUpServerView.as_view(),
        name='wake-up-server'
    )
]
