from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from src.shopping_bags.models import ShoppingBag


@admin.register(ShoppingBag)
class ShoppingBagAdmin(admin.ModelAdmin):
    def product_display(self, obj):
        if obj.inventory:
            product = getattr(obj.inventory, 'product', None)
            if product:
                return str(product)
            return str(obj.inventory)
        return '-'

    product_display.short_description = 'Product'

    def product_info(self, obj):
        if obj.inventory:
            product = getattr(obj.inventory, 'product', None)
            if product:
                app_label = product._meta.app_label
                model_name = product._meta.model_name
                url = reverse(
                    f'admin:{app_label}_{model_name}_change', args=[product.id])
                return format_html('<a href="{}">{}</a>', url, str(product))
            return str(obj.inventory)
        return '-'

    product_info.short_description = 'Product'
    product_info.allow_tags = True

    list_display = (
        'id',
        'user',
        'product_display',
        'quantity',
        'created_at',
    )
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'product_info')
    ordering = ('-created_at',)
    exclude = ('content_type', 'object_id')
