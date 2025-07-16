from typing import Any
from rest_framework import serializers

from src.products.models.review import Review
from src.products.serializers.review import ReviewSerializer


class ReviewManagementSerializer(ReviewSerializer):
    """
    Extended serializer for review management (reviewers only).

    This serializer extends the base ReviewSerializer to include
    approval status and management fields that are only visible
    to users with reviewer permissions.

    Key Features:
    - Includes approval status field
    - Inherits all base review functionality
    - Used only for reviewer-specific endpoints
    """

    # Add approved field for reviewers to see and modify
    approved: serializers.BooleanField = serializers.BooleanField(
        read_only=True)

    class Meta(ReviewSerializer.Meta):
        # Inherit all fields from parent and add approved
        fields = ReviewSerializer.Meta.fields + ['approved']
        read_only_fields = ReviewSerializer.Meta.read_only_fields + \
            ['approved']

    def to_representation(self, instance):
        """
        Custom representation method to include approval status.

        This method ensures that the approval status is always included
        in the serialized output for reviewer management views.

        Args:
            instance: The Review instance being serialized

        Returns:
            dict: Serialized review data with approval status
        """
        data = super().to_representation(instance)
        # Always include approved field for management serializer
        data['approved'] = instance.approved
        return data
