from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from src.products.constants import ReviewFieldLengths

User = get_user_model()


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'content_type', 'object_id')
        permissions = [
            ('approve_review', 'Can approve reviews'),
        ]

    rating = models.IntegerField(
        choices=RATING_CHOICES,
    )

    comment = models.TextField(
        max_length=ReviewFieldLengths.MAX_COMMENT_LENGTH,
        blank=False,
        help_text='Review comment is required.',
    )

    approved = models.BooleanField(
        default=False,
        help_text='Indicates whether the review has been approved by an admin.',
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

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.product} - {self.user.username} ({self.rating})'
