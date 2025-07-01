from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from src.accounts.forms import UserCredentialCreationForm


UserModel = get_user_model()


@admin.register(UserModel)
class UserCredentialAdmin(UserAdmin):
    add_form = UserCredentialCreationForm
    # model = UserModel
    list_display = (
        'pk', 'email', 'username', 'password',
        'is_staff', 'is_superuser'
    )
    search_fields = ('email', 'username')
    ordering = ('pk',)

    fieldsets = (
        (None, {
            'fields': (
                'email', 'password', 'username'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff', 'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': (
                'last_login',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
