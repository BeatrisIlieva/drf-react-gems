from django.db import models


class Label(models.Model):
    LABEL_MAX_LENGTH = 30

    label = models.CharField(
        max_length=LABEL_MAX_LENGTH,
    )
