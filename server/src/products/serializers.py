from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from cloudinary.utils import cloudinary_url
from django.db.models import Avg, Count

from src.products.models.earwear import Earwear
from src.products.models.fingerwear import Fingerwear, FingerwearInventory
from src.products.models.review import Review


class ProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    collection__name = serializers.CharField()
    reference__name = serializers.CharField()
    first_image = serializers.CharField()
    second_image = serializers.CharField()
    price = serializers.DecimalField(max_digits=7, decimal_places=2)
    total_quantity = serializers.IntegerField()
    is_sold_out = serializers.BooleanField()
    materials_count = serializers.IntegerField()
    stones = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(allow_null=True, allow_blank=True)
        )
    )


class EarwearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Earwear
        fields = '__all__'
        depth = 2


class RelatedFingerwearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fingerwear
        fields = ['id', 'first_image']


class FingerwearInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FingerwearInventory
        fields = ['size', 'quantity']
        depth = 2


class FingerwearSerializer(serializers.ModelSerializer):
    inventory = FingerwearInventorySerializer(many=True, read_only=True)
    related_products = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    rating_counts = serializers.SerializerMethodField()

    class Meta:
        model = Fingerwear
        fields = [
            'id',
            'first_image',
            'second_image',
            'price',
            'created_at',
            'collection',
            'material',
            'reference',
            'stone_by_color',
            'inventory',
            'related_products',
            'content_type',
            'reviews',
            'average_rating',
        ]
        depth = 3

    def get_related_products(self, obj):
        related = Fingerwear.objects.filter(
            collection=obj.collection,
            reference=obj.reference
        )

        return RelatedFingerwearSerializer(related, many=True).data

    def get_content_type(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return {
            'content_type_id': content_type.id,
            # 'app_label': content_type.app_label,
            # 'model': content_type.model,
        }

    def get_reviews(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        reviews_qs = Review.objects.filter(
            content_type=content_type,
            object_id=obj.pk
        ).order_by('-created_at')[:5]

        # Serialize the reviews with ReviewSerializer
        return ReviewSerializer(reviews_qs, many=True).data

    def get_average_rating(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        avg = Review.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).aggregate(Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else None



class ReviewSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()

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
        read_only_fields = ['user', 'created_at']

    def get_photo_url(self, obj):
        if obj.user.userphoto.photo:
            return cloudinary_url(obj.user.userphoto.photo.public_id)[0]
        return None

    def get_user_full_name(self, obj):
        if obj.user.userprofile.first_name and obj.user.userprofile.last_name:
            return f'{obj.user.userprofile.first_name} {obj.user.userprofile.last_name}'
        return None
