from cloudinary.utils import cloudinary_url
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from src.products.models.review import Review


class ReviewSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'rating',
            'comment',
            'created_at',
            'content_type',
            'object_id',
            'photo_url',
            'user_full_name'
        ]
        read_only_fields = ['user', 'created_at',
                            'photo_url', 'user_full_name']

    def get_photo_url(self, obj):
        try:
            if obj.user.userphoto.photo:
                return cloudinary_url(obj.user.userphoto.photo.public_id)[0]
        except:
            pass
        return None

    def get_user_full_name(self, obj):
        try:
            if obj.user.userprofile.first_name and obj.user.userprofile.last_name:
                return f'{obj.user.userprofile.first_name} {obj.user.userprofile.last_name}'
        except:
            pass
        return obj.user.username

    def validate_comment(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Comment is required.")
        return value.strip()

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
