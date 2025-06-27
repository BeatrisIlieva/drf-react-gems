from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


UserModel = get_user_model()


class UserCredentialCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email', 'username',)


class UserCredentialChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel
