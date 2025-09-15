from rest_framework.generics import RetrieveUpdateDestroyAPIView

from src.accounts.models.user_profile import UserProfile
from src.accounts.serializers.user_profile import UserProfileSerializer


class UserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)

        return profile
