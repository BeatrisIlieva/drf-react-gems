from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from src.products.models import (
    Earwear,
    Fingerwear,
    Neckwear,
    Wristwear,
    Collection,
    Color,
    Metal,
    Stone,
    Size,
    Inventory,
)
from src.products.models.review import Review


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Metal)
class MetalAdmin(admin.ModelAdmin):
    pass


@admin.register(Stone)
class StoneAdmin(admin.ModelAdmin):
    pass


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    pass


class StoneListFilter(admin.SimpleListFilter):
    title = _('Stone')
    parameter_name = 'stone'

    def lookups(self, request, model_admin):
        return [(s.id, s.name) for s in Stone.objects.all()]

    def queryset(self, request, queryset):
        return (
            queryset.filter(stone__id=self.value())
            if self.value()
            else queryset
        )


class ColorListFilter(admin.SimpleListFilter):
    title = _('Color')
    parameter_name = 'color'

    def lookups(self, request, model_admin):
        return [(c.id, c.name) for c in Color.objects.all()]

    def queryset(self, request, queryset):
        return (
            queryset.filter(color__id=self.value())
            if self.value()
            else queryset
        )


class InventoryInline(GenericTabularInline):
    model = Inventory
    ct_field = "content_type"
    ct_fk_field = "object_id"
    min_num = 1
    max_num = 3
    validate_min = True


class BaseProductAdmin(admin.ModelAdmin):
    list_display = (
        'first_picture',
        'second_picture',
        'collection',
        'created_at',
    )

    list_filter = (StoneListFilter, ColorListFilter, 'collection', 'metal')

    ordering = (
        'created_at',
        'collection',
        'metal',
    )

    search_fields = (
        'collection__name',
        'metal__name',
        'color__name',
        'stone__name',
    )

    fieldsets = (
        ('Images', {'fields': ('first_image', 'second_image')}),
        (
            'Material and Design',
            {
                'fields': (
                    'collection',
                    'metal',
                    'stone',
                    'color',
                )
            },
        ),
    )

    def first_picture(self, obj):
        return format_html(
            '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
            obj.first_image,
        )

    def second_picture(self, obj):
        return format_html(
            '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
            obj.second_image,
        )


@admin.register(Earwear)
class EarwearAdmin(BaseProductAdmin):
    inlines = [InventoryInline]


@admin.register(Neckwear)
class NeckwearAdmin(BaseProductAdmin):
    inlines = [InventoryInline]


@admin.register(Wristwear)
class WristwearAdmin(BaseProductAdmin):
    inlines = [InventoryInline]


@admin.register(Fingerwear)
class FingerwearAdmin(BaseProductAdmin):
    inlines = [InventoryInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'user',
        'rating',
        'approved',
        'created_at',
        'product_link',
    ]
    list_filter = [
        'approved',
        'rating',
        'created_at',
    ]
    search_fields = [
        'user__email',
        'user__userprofile__first_name',
        'user__userprofile__last_name',
        'comment',
    ]
    list_editable = ['approved']
    readonly_fields = [
        'user',
        'rating',
        'comment',
        'created_at',
        'content_type',
        'object_id',
        'product',
    ]
    ordering = ['-created_at']

    def product_link(self, obj):
        if obj.product:
            return format_html(
                '<a href="/admin/products/{}/{}/change/">{}</a>',
                obj.content_type.model,
                obj.object_id,
                str(obj.product),
            )
        return '-'

    product_link.short_description = 'Product'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
