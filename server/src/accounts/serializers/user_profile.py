from src.accounts.models.user_profile import UserProfile
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number']

    def update(self, instance, validated_data):
        """
        Update user profile fields, creating the profile if it doesn't exist
        """
        # Get the user from the instance (which should be the user object)
        user = instance

        # Get or create the user profile
        profile, created = UserProfile.objects.get_or_create(user=user)

        # Update the profile with validated data
        for attr, value in validated_data.items():
            setattr(profile, attr, value)

        profile.save()
        return profile
