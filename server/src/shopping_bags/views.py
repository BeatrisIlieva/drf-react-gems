from rest_framework import viewsets
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
import uuid
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from src.shopping_bags.models import ShoppingBag
from src.shopping_bags.serializers import ShoppingBagSerializer


class ShoppingBagViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingBagSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user if self.request.user.is_authenticated else None
        guest_id = self.request.headers.get('Guest-Id')
        filters = {'user': user} if user else {'guest_id': guest_id}
        return ShoppingBag.objects.filter(**filters)

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        guest_id = self.request.headers.get('Guest-Id')

        if guest_id:
            try:
                guest_id = uuid.UUID(guest_id)
            except ValueError:
                raise ValidationError("Invalid guest ID format.")

        content_type = serializer.validated_data.get('content_type')
        object_id = serializer.validated_data.get('object_id')
        quantity_to_add = serializer.validated_data.get('quantity')

        if not content_type or not object_id or quantity_to_add is None:
            raise ValidationError("Missing required fields.")

        try:
            inventory_obj = content_type.get_object_for_this_type(pk=object_id)
        except content_type.model_class().DoesNotExist:
            raise ValidationError(
                {"object_id": "Invalid object ID for the selected content type."})

        if quantity_to_add > inventory_obj.quantity:
            raise ValidationError("Not enough quantity in inventory.")

        filters = {
            'content_type': content_type,
            'object_id': object_id,
            'user': user,
            'guest_id': guest_id if not user else None,
        }

        existing_item = ShoppingBag.objects.filter(**filters).first()

        if existing_item:
            existing_item.quantity += quantity_to_add
            existing_item.save()
            serializer.instance = existing_item
        else:
            if user:
                serializer.save(user=user)
            else:
                serializer.save(guest_id=guest_id)

        inventory_obj.quantity -= quantity_to_add
        inventory_obj.save()

    def perform_update(self, serializer):
        instance = self.get_object()
        new_quantity = serializer.validated_data.get(
            'quantity', instance.quantity
        )

        inventory_obj = instance.content_type.get_object_for_this_type(
            pk=instance.object_id
        )

        delta = new_quantity - instance.quantity

        if delta > 0:
            if delta > inventory_obj.quantity:
                raise ValidationError("Not enough quantity in inventory.")
            inventory_obj.quantity -= delta

        elif delta < 0:
            if instance.quantity == 1:
                return self.perform_destroy(instance)
            inventory_obj.quantity -= delta

        inventory_obj.save()
        serializer.save()

    def perform_destroy(self, instance):
        inventory_obj = instance.content_type.get_object_for_this_type(
            pk=instance.object_id
        )
        inventory_obj.quantity += instance.quantity
        inventory_obj.save()
        instance.delete()

    @action(detail=False, methods=['get'], url_path='count')
    def get_bag_count(self, request):
        user = request.user if request.user.is_authenticated else None
        guest_id = request.headers.get('Guest-Id')

        if not user:
            try:
                guest_id = uuid.UUID(guest_id)
            except (ValueError, TypeError):
                return Response({'error': 'Invalid or missing Guest-Id'}, status=status.HTTP_400_BAD_REQUEST)

        filters = {'user': user} if user else {'guest_id': guest_id}
        count = ShoppingBag.objects.filter(
            **filters).aggregate(total=Sum('quantity'))['total'] or 0

        return Response({'count': count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='total-price')
    def get_total_price_all(self, request):
        user = request.user if request.user.is_authenticated else None
        guest_id = request.headers.get('Guest-Id')

        if not user:
            try:
                guest_id = uuid.UUID(guest_id)
            except (ValueError, TypeError):
                return Response({'error': 'Invalid or missing Guest-Id'}, status=status.HTTP_400_BAD_REQUEST)

        filters = {'user': user} if user else {'guest_id': guest_id}

        bag_items = ShoppingBag.objects.filter(
            **filters).select_related('content_type')

        total_price = 0.0
        for item in bag_items:
            inventory = item.inventory
            if inventory and hasattr(inventory, 'product'):
                try:
                    total_price += float(inventory.product.price) * \
                        item.quantity
                except Exception:
                    continue

        return Response({'total_price': round(total_price, 2)}, status=status.HTTP_200_OK)
