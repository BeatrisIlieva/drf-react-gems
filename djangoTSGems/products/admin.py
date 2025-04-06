from django.contrib import admin
from djangoTSGems.products.models.products import DropEarring, StudEarring, Necklace, Pendant, Charm, Bracelet, Ring


@admin.register(Bracelet)
class BraceletAdmin(admin.ModelAdmin):
    pass
