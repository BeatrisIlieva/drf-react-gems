from src.accounts.models.user_profile import UserProfile
from src.accounts.serializers.user_profile import UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get user profile information
        """
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            # Return empty profile data if profile doesn't exist yet
            return Response({
                'first_name': '',
                'last_name': '',
                'phone_number': ''
            }, status=status.HTTP_200_OK)

    def patch(self, request):
        """
        Update user profile information
        """
        serializer = UserProfileSerializer(
            request.user, data=request.data, partial=True)

        if serializer.is_valid():
            profile = serializer.save()
            response_serializer = UserProfileSerializer(profile)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
