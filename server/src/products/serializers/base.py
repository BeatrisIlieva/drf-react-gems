from typing import Any, Dict, Type, Optional
from django.db.models import Avg

from rest_framework import serializers

from src.products.serializers.inventory import InventorySerializer
from src.products.serializers.review import ReviewSerializer
from src.products.models.product import Earwear, Neckwear, Fingerwear, Wristwear


class BaseProductListSerializer(serializers.ModelSerializer):
    average_rating: serializers.DecimalField = serializers.DecimalField(
        max_digits=7,
        decimal_places=2,
    )
    is_sold_out: serializers.BooleanField = serializers.BooleanField()
    collection__name: serializers.CharField = serializers.CharField()
    color__name: serializers.CharField = serializers.CharField()
    stone__name: serializers.CharField = serializers.CharField()
    metal__name: serializers.CharField = serializers.CharField()
    min_price: serializers.DecimalField = serializers.DecimalField(
        max_digits=7,
        decimal_places=2,
    )
    max_price: serializers.DecimalField = serializers.DecimalField(
        max_digits=7,
        decimal_places=2,
    )

    class Meta:
        fields: list[str] = [
            'id',
            'first_image',
            'second_image',
            'collection__name',
            'color__name',
            'stone__name',
            'metal__name',
            'is_sold_out',
            'average_rating',
            'min_price',
            'max_price'
        ]
        depth = 2


class AverageRatingField(serializers.Field):
    def to_representation(
        self,
        value: Any
    ) -> float:
        avg: float = value.review.filter(approved=True).aggregate(
            avg=Avg('rating'))['avg'] or 0
        return round(avg, 2)


class RelatedProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields: list[str] = ['id', 'first_image']
        model: Optional[Type[Any]] = None


class BaseProductItemSerializer(serializers.ModelSerializer):
    inventory: InventorySerializer = InventorySerializer(many=True, read_only=True)
    review: serializers.SerializerMethodField = serializers.SerializerMethodField()
    average_rating: AverageRatingField = AverageRatingField(source='*')
    related_collection_products: serializers.SerializerMethodField = serializers.SerializerMethodField()
    related_products: serializers.SerializerMethodField = serializers.SerializerMethodField()

    class Meta:
        fields: str = '__all__'
        depth = 2

    def get_review(
        self,
        obj: Any
    ) -> Any:
        latest_reviews = obj.review.filter(approved=True)[:6]
        return ReviewSerializer(latest_reviews, many=True).data

    def get_related_collection_products(
        self,
        obj: Any
    ) -> Any:
        model_class: Type[Any] = obj.__class__
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

    def get_related_products(
        self,
        obj: Any
    ) -> list[Dict[str, Any]]:
        color_id: Any = obj.color_id
        def serialize_products_of_type(
            model_class: Type[Any],
            is_current_type: bool
        ) -> list[Dict[str, Any]]:
            products = model_class.objects.filter(color_id=color_id)
            if is_current_type:
                products = products.exclude(id=obj.id)
            result: list[Dict[str, Any]] = []
            for product in products:
                result.append({
                    'id': product.id,
                    'first_image': product.first_image,
                    'product_type': f'{model_class.__name__.lower()}s',
                })
            return result
        current_product_type: Type[Any] = type(obj)
        related_products: list[Dict[str, Any]] = []
        related_products.extend(serialize_products_of_type(
            Earwear, current_product_type == Earwear))
        related_products.extend(serialize_products_of_type(
            Neckwear, current_product_type == Neckwear))
        related_products.extend(serialize_products_of_type(
            Fingerwear, current_product_type == Fingerwear))
        related_products.extend(serialize_products_of_type(
            Wristwear, current_product_type == Wristwear))
        return related_products[:6]


class BaseAttributesSerializer(serializers.ModelSerializer):
    count: serializers.IntegerField = serializers.IntegerField()

    class Meta:
        fields: list[str] = ['id', 'name', 'count']
