from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'content_type', 'object_id')

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )

    rating = models.IntegerField(
        choices=RATING_CHOICES,
    )

    comment = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    object_id = models.PositiveIntegerField()

    product = GenericForeignKey(
        'content_type',
        'object_id',
    )

    def __str__(self):
        return f'{self.product} - {self.user.username} ({self.rating})'
