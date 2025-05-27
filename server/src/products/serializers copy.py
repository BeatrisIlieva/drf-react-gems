from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from cloudinary.utils import cloudinary_url
from django.db.models import Avg

from src.products.models.earwear import Earwear, EarwearInventory
from src.products.models.fingerwear import Fingerwear, FingerwearInventory
from src.products.models.neckwear import Neckwear, NeckwearInventory
from src.products.models.review import Review
from src.products.models.wristwear import Wristwear, WristwearInventory


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


class BaseProductItemSerializer(serializers.ModelSerializer):
    related_products = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    base_fields = [
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

    class Meta:
        abstract = True
        depth = 3

    def get_related_products(self, obj):
        model = self.Meta.model
        serializer_class = self.related_serializer_class

        related = model.objects.filter(
            collection=obj.collection,
            reference=obj.reference
        )[:4]

        return serializer_class(related, many=True).data

    def get_content_type(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return {'content_type_id': content_type.id}

    def get_reviews(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        reviews_qs = Review.objects.filter(
            content_type=content_type,
            object_id=obj.pk
        ).order_by('-created_at')[:4]

        return ReviewSerializer(reviews_qs, many=True).data

    def get_average_rating(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        avg = Review.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).aggregate(Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else None


class SizedInventorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['size', 'quantity']
        depth = 2


class SimpleInventorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['quantity']
        depth = 2


class RelatedFingerwearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fingerwear
        fields = ['id', 'first_image']


class FingerwearInventorySerializer(SizedInventorySerializer):
    class Meta(SizedInventorySerializer.Meta):
        model = FingerwearInventory


class FingerwearSerializer(BaseProductItemSerializer):
    inventory = FingerwearInventorySerializer(many=True, read_only=True)
    related_serializer_class = RelatedFingerwearSerializer

    class Meta(BaseProductItemSerializer.Meta):
        model = Fingerwear
        fields = BaseProductItemSerializer.base_fields


class RelatedWristwearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wristwear
        fields = ['id', 'first_image']


class WristwearInventorySerializer(SizedInventorySerializer):
    class Meta(SizedInventorySerializer.Meta):
        model = WristwearInventory


class WristwearSerializer(BaseProductItemSerializer):
    inventory = WristwearInventorySerializer(many=True, read_only=True)
    related_serializer_class = RelatedWristwearSerializer

    class Meta(BaseProductItemSerializer.Meta):
        model = Wristwear
        fields = BaseProductItemSerializer.base_fields


class RelatedNeckwearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neckwear
        fields = ['id', 'first_image']


class NeckwearInventorySerializer(SizedInventorySerializer):
    class Meta(SizedInventorySerializer.Meta):
        model = NeckwearInventory


class NeckwearSerializer(BaseProductItemSerializer):
    inventory = NeckwearInventorySerializer(many=True, read_only=True)
    related_serializer_class = RelatedNeckwearSerializer

    class Meta(BaseProductItemSerializer.Meta):
        model = Neckwear
        fields = BaseProductItemSerializer.base_fields


class RelatedEarwearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Earwear
        fields = ['id', 'first_image']


class EarwearInventorySerializer(SimpleInventorySerializer):
    class Meta(SimpleInventorySerializer.Meta):
        model = EarwearInventory


class EarwearSerializer(BaseProductItemSerializer):
    inventory = EarwearInventorySerializer(read_only=True)
    related_serializer_class = RelatedEarwearSerializer

    class Meta(BaseProductItemSerializer.Meta):
        model = Earwear
        fields = BaseProductItemSerializer.base_fields
