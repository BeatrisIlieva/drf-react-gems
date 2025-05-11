from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

# from src.accounts.forms import UserCredentialChangeForm, UserCredentialCreationForm

UserModel = get_user_model()

# @admin.register(UserModel)
# class UserCredentialAdmin(UserAdmin):
#     model = UserModel
#     # add_form = UserCredentialCreationForm
#     # form = UserCredentialChangeForm
#     list_display = ('pk', 'email', 'is_staff', 'is_superuser')
#     search_fields = ('email',)
#     ordering = ('pk',)
    
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         # ('Personal info', {'fields': ('first_name', 'last_name')}), 
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login',)}),
#     )
    
#     # add_fieldsets = (
#     #     (None, {
#     #         "classes": ("wide",),
#     #         "fields": ("email", "password1", "password2"),
#     #     }),
#     # )


@admin.register(UserModel)
class UserCredentialAdmin(UserAdmin):
    model = UserModel
    list_display = ('pk', 'email', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('pk',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
