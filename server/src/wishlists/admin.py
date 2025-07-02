from django.contrib import admin

from src.wishlists.models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'guest_id', 'product', 'created_at']
    list_filter = ['created_at', 'content_type']
    search_fields = ['user__email', 'guest_id']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'content_type')
