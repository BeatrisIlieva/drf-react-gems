from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from src.wishlists.models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    def product_display(self, obj):
        if obj.product:
            return str(obj.product)

        return '-'

    product_display.short_description = 'Product'

    def product_info(self, obj):
        if obj.product:
            app_label = obj.product._meta.app_label
            model_name = obj.product._meta.model_name
            url = reverse(
                f'admin:{app_label}_{model_name}_change', args=[obj.product.id]
            )
            return format_html('<a href="{}">{}</a>', url, str(obj.product))

        return '-'

    product_info.short_description = 'Product'
    product_info.allow_tags = True

    list_display = (
        'id',
        'user',
        'product_display',
        'created_at',
    )
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'product_info')
    ordering = ('-created_at',)
    exclude = ('content_type', 'object_id')
