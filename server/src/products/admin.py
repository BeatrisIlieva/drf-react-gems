from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from src.products.models.relationships.collection import Collection
from src.products.models.relationships.material import Material
from src.products.models.relationships.reference import Reference
from src.products.models.relationships.size import ProductSize, Size
from src.products.models.relationships.category import Category
from src.products.models.relationships.stone_by_color import StoneByColor
from src.products.models import Product
from src.products.models.relationships.color import Color
from src.products.models.relationships.stone import Stone


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


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


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(StoneByColor)
class StoneByColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Stone)
class StoneAdmin(admin.ModelAdmin):
    pass


class StoneListFilter(admin.SimpleListFilter):

    title = _('Stone')
    parameter_name = 'stone'

    def lookups(self, request, model_admin):
        stones = Stone.objects.all()
        return [(stone.id, stone.name) for stone in stones]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(stone_by_color__stone__id=self.value()).distinct()
        return queryset


class ColorListFilter(admin.SimpleListFilter):
    title = _('Color')
    parameter_name = 'color'

    def lookups(self, request, model_admin):
        colors = Color.objects.all()
        return [(color.id, color.name) for color in colors]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(stone_by_color__color__id=self.value()).distinct()
        return queryset
    

    
class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    max_num = 1  
    min_num = 1
    validate_min = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductSizeInline]

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

    ordering = (
        'collection',
        'reference',
        'category',
        'material',
    )

    search_fields = (
        'category__name',
        'collection__name',
        'reference__name',
        'stone_by_color__color__name',
        'stone_by_color__stone__name',
    )

    fieldsets = (
        ('Images', {
            'fields': (
                'first_image',
                'second_image',
            )
        }),
        ('Material and Design', {
            'fields': (
                'category',
                'collection',
                'reference',
                'material',
                'stone_by_color',
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
