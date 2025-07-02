from django.db import transaction
from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from src.shopping_bags.models import ShoppingBag
from src.shopping_bags.serializers import ShoppingBagSerializer
from src.shopping_bags.services import ShoppingBagService


class ShoppingBagViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingBagSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        try:
            user_filters = ShoppingBagService.get_user_identifier(self.request)
            return ShoppingBag.objects.filter(**user_filters).select_related(
                'content_type', 'user'
            ).prefetch_related('inventory')
        except ValidationError:
            return ShoppingBag.objects.none()

    @transaction.atomic
    def perform_create(self, serializer):
        user_filters = ShoppingBagService.get_user_identifier(self.request)
        validated_data = serializer.validated_data

        content_type = validated_data['content_type']
        object_id = validated_data['object_id']
        quantity_to_add = validated_data['quantity']

        inventory_obj = ShoppingBagService.get_inventory_object(
            content_type, object_id)
        ShoppingBagService.validate_inventory_quantity(
            inventory_obj, quantity_to_add)

        filters = {
            'content_type': content_type,
            'object_id': object_id,
            **user_filters
        }

        bag_item, created = ShoppingBagService.get_or_create_bag_item(
            filters=filters,
            defaults={'quantity': quantity_to_add}
        )

        if not created:
            new_total_quantity = bag_item.quantity + quantity_to_add
            ShoppingBagService.validate_inventory_quantity(
                inventory_obj, quantity_to_add)
            bag_item.quantity = new_total_quantity
            bag_item.save(update_fields=['quantity'])

        ShoppingBagService.update_inventory_quantity(
            inventory_obj, quantity_to_add)
        serializer.instance = bag_item

    @transaction.atomic
    def perform_update(self, serializer):
        instance = self.get_object()
        new_quantity = serializer.validated_data.get(
            'quantity', instance.quantity)

        if new_quantity <= 0:
            return self.perform_destroy(instance)

        inventory_obj = ShoppingBagService.get_inventory_object(
            instance.content_type, instance.object_id
        )

        quantity_delta = new_quantity - instance.quantity

        if quantity_delta > 0:
            ShoppingBagService.validate_inventory_quantity(
                inventory_obj, quantity_delta)

        ShoppingBagService.update_inventory_quantity(
            inventory_obj, quantity_delta)
        serializer.save()

    @transaction.atomic
    def perform_destroy(self, instance):
        inventory_obj = ShoppingBagService.get_inventory_object(
            instance.content_type, instance.object_id
        )

        ShoppingBagService.update_inventory_quantity(
            inventory_obj, -instance.quantity)
        instance.delete()

    @action(detail=False, methods=['get'], url_path='count')
    def get_bag_count(self, request):
        try:
            user_filters = ShoppingBagService.get_user_identifier(request)
            count = ShoppingBag.objects.filter(**user_filters).aggregate(
                total=Sum('quantity')
            )['total'] or 0

            return Response({'count': count}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='total-price')
    def get_total_price(self, request):
        try:
            user_filters = ShoppingBagService.get_user_identifier(request)
            bag_items = ShoppingBag.objects.filter(**user_filters).select_related(
                'content_type'
            )

            total_price = sum(
                float(item.inventory.price) * item.quantity
                for item in bag_items
                if item.inventory and hasattr(item.inventory, 'price')
            )

            return Response({
                'total_price': round(total_price, 2)
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({
                'error': 'Unable to calculate total price'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
