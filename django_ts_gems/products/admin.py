from django.contrib import admin
from django.utils.html import format_html

from django_ts_gems.products.models import Product
from django_ts_gems.products.models.relationships.description import Description
from django_ts_gems.products.models.relationships.media import Media


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'image',
        'category',
        'collection',
        'primary_stone',
        'reference',
    )
    list_filter = (
        'category',
        'category',
        'collection',
        'primary_stone',
        'reference',
    )

    fieldsets = (
        ('Summary', {
            'fields': (
                'description',
            )
        }),
        ('Images', {
            'fields': (
                'media',
            )
        }),
        ('Labels', {
            'fields': (
                'category',
                'collection',
                'reference',
            )
        }
        ),
        ('Materials', {
            'fields': (
                'primary_stone',
                'stones',
                'colors',
                'materials',
            )
        }),
    )

    def image(self, obj):
        return format_html(
            '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
            obj.media.first_image)

    def category(self, obj):
        return obj.category.get_category_display()

    def collection(self, obj):
        return obj.category.get_collection_display()

    def primary_stone(self, obj):
        return obj.category.get_primary_stone_display()

    def obj_description(self, obj):
        return obj.description.description


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    fields = (
        'first_image',
        'second_image',
        'third_image',
        'fourth_image',
        'fifth_image',
    )


@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    pass
