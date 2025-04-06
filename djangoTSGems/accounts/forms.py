from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from djangoTSGems.accounts.models import AppPayment

from django import forms


UserModel = get_user_model()


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel

class PaymentForm(forms.ModelForm):
    
    class Meta:
        model = AppPayment
        fields = '__all__'
        
    # error_messages = {
    #     'card_holder': {
    #         'invalid': 'asd',
    #         'password_mismatch': 'asd',
    #     }
    # }
        

# class PaymentForm(forms.Form):
#     RADIO_CHOICES = (
#         (1, 'first'),
#         (2, 'second'),
#         (3, 'third'),
#     )

#     CHECKBOX_CHOICES = (
#         (1, 'first'),
#         (2, 'second'),
#         (3, 'third'),
#     )

#     card_holder = forms.CharField(
#         label='Card Holder enter',
#         widget=forms.TextInput(attrs={'placeholder': 'Search'}),
#         error_messages={
#             'invalid': 'asd'
#         },
#     )
#     card_number = forms.CharField()
#     expiry_date = forms.CharField()
#     cvv_code = forms.CharField()

#     radio_choice = forms.ChoiceField(
#         widget=forms.RadioSelect,
#         choices=RADIO_CHOICES,
#     )

#     checkbox_choice = forms.MultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple,
#         choices=CHECKBOX_CHOICES,
#     )
