from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from src.shopping_bag.models import ShoppingBag
from src.shopping_bag.serializers import ShoppingBagSerializer


class ShoppingBagViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingBagSerializer

    def get_queryset(self):
        return ShoppingBag.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user

        content_type = serializer.validated_data.get('content_type')
        object_id = serializer.validated_data.get('object_id')
        quantity_to_add = serializer.validated_data.get('quantity')

        if not content_type:
            raise ValidationError({"content_type": "This field is required."})
        if not object_id:
            raise ValidationError({"object_id": "This field is required."})
        if quantity_to_add is None:
            raise ValidationError({"quantity": "This field is required."})

        try:
            inventory_obj = content_type.get_object_for_this_type(pk=object_id)
        except content_type.model_class().DoesNotExist:
            raise ValidationError(
                {"object_id": "Invalid object ID for the selected content type."})

        if quantity_to_add > inventory_obj.quantity:
            raise ValidationError("Not enough quantity in inventory.")

        existing_item = ShoppingBag.objects.filter(
            user=user,
            content_type=content_type,
            object_id=object_id
        ).first()

        if existing_item:
            existing_item.quantity += quantity_to_add
            existing_item.save()
            serializer.instance = existing_item
        else:
            serializer.save(user=user)

        inventory_obj.quantity -= quantity_to_add
        inventory_obj.save()

    def perform_update(self, serializer):
        instance = self.get_object()
        new_quantity = serializer.validated_data.get(
            'quantity', instance.quantity)

        inventory_obj = instance.content_type.get_object_for_this_type(
            pk=instance.object_id)

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
            pk=instance.object_id)
        inventory_obj.quantity += instance.quantity
        inventory_obj.save()
        instance.delete()
