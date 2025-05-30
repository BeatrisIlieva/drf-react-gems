from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
from rest_framework import serializers

from src.products.models.review import Review
from src.products.serializers.review import ReviewSerializer


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
