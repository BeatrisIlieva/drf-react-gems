from rest_framework import serializers
from src.accounts.models.user_address import UserAddress


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [
            'apartment', 'country', 'city', 'street_address', 'zip_code',

        ]

    def update(self, instance, validated_data):
        user = instance

        address, _ = UserAddress.objects.get_or_create(user=user)

        for attr, value in validated_data.items():
            setattr(address, attr, value)

        address.save()
        return address
