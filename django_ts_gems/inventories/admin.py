# from django import forms
# from django.contrib import admin
# from .models import Inventory

# class InventoryAdminForm(forms.ModelForm):
#     class Meta:
#         model = Inventory
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Only run this when an instance is already selected
#         instance = kwargs.get('instance')
#         if instance:
#             product_model = instance.content_type.model_class()
#             if product_model not in [Bracelet, Ring, Necklace]:
#                 self.fields['size'].widget = forms.HiddenInput()
