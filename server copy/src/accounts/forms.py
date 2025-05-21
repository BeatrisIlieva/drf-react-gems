from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms


UserModel = get_user_model()


class UserCredentialCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)


class UserCredentialChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel