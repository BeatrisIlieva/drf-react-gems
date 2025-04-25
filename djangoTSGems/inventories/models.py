from django.db import models


from django.core.exceptions import ValidationError

from djangoTSGems.products.models.size import Size

class Inventory(models.Model):
    class Meta:
        unique_together = ('content_type', 'object_id', 'size')
        
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')

    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # def clean(self):
    #     # Dynamically determine if this product requires size
    #     model_class = self.content_type.model_class()
    #     requires_size = model_class in [Bracelet, Ring, Necklace]  # Add any size-based products here

    #     if requires_size and self.size is None:
    #         raise ValidationError("This product requires a size.")
    #     elif not requires_size and self.size is not None:
    #         raise ValidationError("This product should not have a size.")
