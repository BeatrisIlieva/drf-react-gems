from django.db import models


class Description(models.Model):
    DESCRIPTION_MAX_LENGTH = 300

    content = models.TextField(
        max_length=DESCRIPTION_MAX_LENGTH,
    )
