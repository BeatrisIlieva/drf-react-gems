from rest_framework import serializers

from cloudinary.utils import cloudinary_url

from ..models.user_photo import UserPhoto


class PhotoSerializer(serializers.ModelSerializer):
    # photo_url is a computed field, not stored in the model.
    # It returns the URL to the image hosted on Cloudinary.
    photo_url = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserPhoto
        # Include user, photo (the file), and photo_url (the URL for display)
        fields: list[str] = [
            'user',
            'photo',
            'photo_url'
        ]
        # user is read-only; it should not be set by the client
        read_only_fields: list[str] = [
            'user'
        ]

    def get_photo_url(
        self,
        obj: UserPhoto
    ) -> str | None:
        """
        Returns the URL to the uploaded photo using Cloudinary.
        This allows the frontend to display the image by URL.
        If no photo is present, returns None.
        """
        if obj.photo:
            # cloudinary_url returns a tuple; [0] is the actual URL string
            return cloudinary_url(obj.photo.public_id)[0]
        return None
