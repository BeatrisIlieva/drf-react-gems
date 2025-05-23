from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from src.products.models.relationships.collection import Collection
from src.products.models.relationships.material import Material
from src.products.models.relationships.reference import Reference
from src.products.models.relationships.stone_by_color import StoneByColor
from src.products.models.relationships.color import Color
from src.products.models.relationships.stone import Stone

from src.products.models.earwear import Earwear, EarwearInventory
from src.products.models.fingerwear import (
    Fingerwear,
    FingerwearInventory,
    FingerwearSize
)
from src.products.models.wristwear import (
    Wristwear,
    WristwearInventory,
    WristwearSize
)
from src.products.models.neckwear import (
    Neckwear,
    NeckwearSize,
    NeckwearInventory
)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    pass


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    pass


@admin.register(StoneByColor)
class StoneByColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Stone)
class StoneAdmin(admin.ModelAdmin):
    pass


@admin.register(FingerwearSize)
class FingerwearSizeAdmin(admin.ModelAdmin):
    pass


@admin.register(WristwearSize)
class WristwearSizeAdmin(admin.ModelAdmin):
    pass


@admin.register(NeckwearSize)
class NeckwearSizeSizeAdmin(admin.ModelAdmin):
    pass


class StoneListFilter(admin.SimpleListFilter):
    title = _('Stone')
    parameter_name = 'stone'

    def lookups(self, request, model_admin):
        return [(s.id, s.name) for s in Stone.objects.all()]

    def queryset(self, request, queryset):
        return queryset.filter(stone_by_color__stone__id=self.value()) if self.value() else queryset


class ColorListFilter(admin.SimpleListFilter):
    title = _('Color')
    parameter_name = 'color'

    def lookups(self, request, model_admin):
        return [(c.id, c.name) for c in Color.objects.all()]

    def queryset(self, request, queryset):
        return queryset.filter(stone_by_color__color__id=self.value()) if self.value() else queryset


class EarwearInventoryInline(admin.TabularInline):
    model = EarwearInventory
    min_num = 1
    max_num = 1
    validate_min = True


class NeckwearInventoryInline(admin.TabularInline):
    model = NeckwearInventory
    min_num = 1
    max_num = 1
    validate_min = True


class FingerInventoryInline(admin.TabularInline):
    model = FingerwearInventory
    min_num = 1
    max_num = 1
    validate_min = True


class WristInventoryInline(admin.TabularInline):
    model = WristwearInventory
    min_num = 1
    max_num = 1
    validate_min = True


class BaseProductAdmin(admin.ModelAdmin):
    list_display = (
        'first_picture',
        'second_picture',
        'collection',
        'reference',
        'created_at',
    )

    list_filter = (
        StoneListFilter,
        ColorListFilter,
        'collection',
        'reference',
        'material'
    )

    ordering = (
        'collection',
        'reference',
        'material',
        'created_at'
    )

    search_fields = (
        'collection__name',
        'reference__name',
        'material__name',
        'stone_by_color__color__name',
        'stone_by_color__stone__name',
    )

    fieldsets = (
        ('Images',
         {
             'fields': (
                 'first_image',
                 'second_image'
             )
         }),
        ('Material and Design',
         {
             'fields': (
                 'collection',
                 'reference',
                 'material',
                 'stone_by_color'
             )
         }),
    )

    def first_picture(self, obj):
        return format_html(
            '<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.first_image
        )

    def second_picture(self, obj):
        return format_html(
            '<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.second_image
        )


@admin.register(Neckwear)
class NeckwearAdmin(BaseProductAdmin):
    inlines = [NeckwearInventoryInline]


@admin.register(Fingerwear)
class FingerwearAdmin(BaseProductAdmin):
    inlines = [FingerInventoryInline]


@admin.register(Wristwear)
class WristwearAdmin(BaseProductAdmin):
    inlines = [WristInventoryInline]


@admin.register(Earwear)
class EarwearAdmin(BaseProductAdmin):
    inlines = [EarwearInventoryInline]
