from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from src.accounts.models.user_address import UserAddress
from src.accounts.serializers.user_address import UserAddressSerializer


class UserAddressView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        address, _ = UserAddress.objects.get_or_create(
            user=self.request.user
        )

        return address
