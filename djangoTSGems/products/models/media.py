from django.db import models


class Media(models.Model):
    first_image = models.URLField()

    second_image = models.URLField()

    third_image = models.URLField()

    fourth_image = models.URLField()
    
