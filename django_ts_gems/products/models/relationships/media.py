from django.db import models


class Media(models.Model):
    
    class Meta:
        verbose_name_plural = 'Media'

    first_image = models.URLField()

    second_image = models.URLField()

    third_image = models.URLField()

    fourth_image = models.URLField()
    
    fifth_image = models.URLField()

    def __str__(self):
        return f'ID: {self.pk}'
