from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html

from django_ts_gems.inventories.models import Inventory
from django_ts_gems.products.models import Product
from django_ts_gems.products.models.relationships.color import Color
from django_ts_gems.products.models.relationships.stone import Stone
from django_ts_gems.products.models.size import Size


class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('size', 'price', 'quantity')
        }),
    )


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


@admin.register(Size)
class SizeAdmin(ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    inlines = [InventoryInline]

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

    search_fields = ('category__category',)

    readonly_fields = ('description', 'stones', 'colors',)

    fieldsets = (
        (None, {
            'fields': (
                'description',
            )
        }),
        (None, {
            'fields': (
                'category',
                'collection',
                'reference',
            )
        }
        ),
        (None, {
            'fields': (
                'material',
            )
        }),
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
