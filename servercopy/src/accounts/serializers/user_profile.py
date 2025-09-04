from rest_framework import serializers

from src.accounts.models.user_profile import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['user']

    def update(self, instance, validated_data):
        user = instance

        profile, _ = UserProfile.objects.get_or_create(user=user)

        for attr, value in validated_data.items():
            setattr(profile, attr, value)

        profile.save()

        return profile
