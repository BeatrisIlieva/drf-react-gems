from src.accounts.models.user_profile import UserProfile
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'apartment',
            'country',
            'city',
            'street_address',
            'zip_code',
        ]

    def update(self, instance, validated_data):
        user = instance

        profile, _ = UserProfile.objects.get_or_create(user=user)

        for attr, value in validated_data.items():
            setattr(profile, attr, value)

        profile.save()
        return profile
