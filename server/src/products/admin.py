from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html

from src.products.models.product_item import ProductItemStonesColors
from src.products.models.product_variant import ProductVariant
from src.products.models import ProductItem
from src.products.models.characteristics.color import Color
from src.products.models.characteristics.stone import Stone


class StoneListFilter(admin.SimpleListFilter):

    title = _('Stone')
    parameter_name = 'stone'

    def lookups(self, request, model_admin):
        stones = Stone.objects.all()
        return [(stone.id, stone.name) for stone in stones]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(stones_colors__stone__id=self.value()).distinct()
        return queryset


class ColorListFilter(admin.SimpleListFilter):
    title = _('Color')
    parameter_name = 'color'

    def lookups(self, request, model_admin):
        colors = Color.objects.all()
        return [(color.id, color.name) for color in colors]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(stones_colors__color__id=self.value()).distinct()
        return queryset


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class ProductItemStonesColorsInline(admin.TabularInline):
    model = ProductItemStonesColors
    extra = 1


@admin.register(ProductItem)
class ProductAdmin(ModelAdmin):
    inlines = [ProductVariantInline, ProductItemStonesColorsInline]

    list_display = (
        'first_picture',
        'second_picture',
        'category',
        'collection',
        'reference',
    )

    list_filter = (
        StoneListFilter,
        ColorListFilter,
        'category',
        'collection',
        'reference',
        'material',
    )

    ordering = ('material', 'category', 'collection', 'reference',)

    search_fields = ('category__name', 'color__name', 'stone__name',)

    readonly_fields = ('description', 'stones', 'colors',)

    fieldsets = (
        (None, {
            'fields': (
                'description',
            )
        }),
        ('Images', {
            'fields': (
                'first_image',
                'second_image',
            )
        }),
        ('Characteristics', {
            'fields': (
                'category',
                'collection',
                'reference',
                'material',
            )
        }
        ),
    )

    def first_picture(self, obj):
        return format_html(
            '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
            obj.first_image
        )

    def second_picture(self, obj):
        return format_html(
            '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
            obj.second_image
        )

    def stones(self, obj):
        stones = obj.stones_colors.select_related('stone')

        return stones

    def colors(self, obj):
        colors = obj.stones_colors.select_related('color')

        return colors

    def description(self, obj):
        stones_colors = []

        for el in obj.stones_colors.select_related('stone', 'color').all():
            stones_colors.append(f'{el.color.name} {el.stone.name}')

        string = ''

        if len(stones_colors) > 1:
            for i, el in enumerate(stones_colors):
                if i == len(stones_colors) - 2:
                    string += f'{el}s and {stones_colors[i + 1]}s'

                    break
                else:
                    string += f'{el}s, '
        else:
            string += stones_colors[0] + 's'

        return string + f' set in {obj.material}.'
