from django.core.validators import MinValueValidator

from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ShoppingBag(models.Model):
    QUANTITY_MIN_VALUE = 1

    quantity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(QUANTITY_MIN_VALUE),
        ]
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )
