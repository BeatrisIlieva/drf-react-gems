
from django.db import models

from django_ts_gems.products.choices import CategoryChoices


class Category(models.Model):

    category = models.CharField(
        max_length=CategoryChoices.max_length(),
        choices=CategoryChoices.choices,
        unique=True,
        error_messages={
            'unique': 'This category already exists.'
        }
    )

    def __str__(self):
        return self.get_category_display()
