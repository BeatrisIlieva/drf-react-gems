"""
This module contains base and shared serializers for product-related API endpoints.

It provides:
- Base serializers for product lists and product detail views
- Logic for calculating average ratings and handling related products
- Shared fields and methods for reuse and extension in the product app
"""

from django.db.models import Avg, Q, F

from rest_framework import serializers

from src.products.models.product import Bracelet, Earring, Necklace, Pendant, Ring, Watch
from src.products.serializers.inventory import InventorySerializer
from src.products.serializers.review import ReviewSerializer


class BaseProductListSerializer(serializers.ModelSerializer):
    average_rating = serializers.DecimalField(
        max_digits=7,
        decimal_places=2,
    )
    is_sold_out = serializers.BooleanField()
    collection__name = serializers.CharField()
    color__name = serializers.CharField()
    stone__name = serializers.CharField()
    metal__name = serializers.CharField()
    min_price = serializers.DecimalField(
        max_digits=7,
        decimal_places=2,
    )
    max_price = serializers.DecimalField(
        max_digits=7,
        decimal_places=2,
    )

    class Meta:
        fields = [
            'id',
            'first_image',
            'second_image',
            'third_image',
            'fourth_image',
            'description',
            'collection__name',
            'color__name',
            'stone__name',
            'metal__name',
            'average_rating',
            'min_price',
            'max_price',
        ]
        depth = 2


class AverageRatingField(serializers.Field):
    def to_representation(self, value):
        # Always calculate average from approved reviews only
        # This ensures consistency across all users
        avg = (
            value.review.filter(
                approved=True,
            ).aggregate(
                avg=Avg('rating'),
            )['avg']
            or 0
        )

        return round(avg, 2)


class RelatedProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'id',
            'first_image',
        ]
        model = None


class BaseProductItemSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(many=True, read_only=True)
    review = serializers.SerializerMethodField()
    average_rating = AverageRatingField(source='*')
    related_collection_products = serializers.SerializerMethodField()
    related_products = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        depth = 2

    def get_review(self, obj):
        # Get the request from context to check user permissions
        request = self.context.get('request')

        # If user is a reviewer, show all reviews (approved and unapproved)
        if request and request.user.has_perm('products.approve_review'):
            latest_reviews = obj.review.all()[:6]
        else:
            # Regular users only see approved reviews
            latest_reviews = obj.review.filter(approved=True)[:6]

        return ReviewSerializer(latest_reviews, many=True).data

    def get_related_collection_products(self, obj):
        model_class = obj.__class__
        related_products = model_class.objects.filter(
            collection=obj.collection
        )

        class DynamicRelatedProductSerializer(RelatedProductSerializer):
            class Meta(RelatedProductSerializer.Meta):
                model = model_class

        serializer = DynamicRelatedProductSerializer(
            related_products, many=True
        )

        return serializer.data

    def get_related_products(self, obj):
        color_id = obj.color_id
        target_gender = obj.target_gender
        current_product_type = type(obj)
        related_products = []

        def serialize_products_of_type(model_class):
            # Only include products from other types
            if model_class == current_product_type and target_gender != 'M':
                return []

            if target_gender == 'M':
                products = model_class.objects.filter(
                    Q(target_gender=target_gender)
                )
            else:
                products = model_class.objects.filter(
                    color_id=color_id,
                )
                
            result = []
            for product in products:
                result.append(
                    {
                        'id': product.id,
                        'first_image': product.first_image,
                        'product_type': f'{model_class.__name__.lower()}s',
                    }
                )
            return result

        related_products.extend(serialize_products_of_type(Earring))
        related_products.extend(serialize_products_of_type(Necklace))
        related_products.extend(serialize_products_of_type(Pendant))
        related_products.extend(serialize_products_of_type(Ring))
        related_products.extend(serialize_products_of_type(Bracelet))
        related_products.extend(serialize_products_of_type(Watch))

        return related_products[:5]


class BaseAttributesSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        fields = [
            'id',
            'name',
            'count',
        ]
