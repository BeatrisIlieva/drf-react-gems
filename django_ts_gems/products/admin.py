# from django.contrib import admin
# from unfold.admin import ModelAdmin
# from django.utils.html import format_html

# from django_ts_gems.products.models import Product


# @admin.register(Product)
# class ProductAdmin(ModelAdmin):
#     list_display = (
#         'image',
#         'category',
#         'collection',
#         'reference',
#     )

#     list_filter = (
#         'category',
#         'collection',
#         'reference',
#     )

#     ordering = ('materials', 'collection',)

#     search_fields = ('category__category',)

#     fieldsets = (
#         # ('Summary', {
#         #     'fields': (
#         #         'description',
#         #     )
#         # }),
#         ('Images', {
#             'fields': (
#                 'media',
#             )
#         }),
#         ('Labels', {
#             'fields': (
#                 'category',
#                 'collection',
#                 'reference',
#             )
#         }
#         ),
#         ('Materials', {
#             'fields': (
#                 'stones',
#                 'colors',
#                 'materials',
#             )
#         }),
#     )

#     def image(self, obj):
#         return format_html(
#             '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
#             obj.media.first_image)

#     def category(self, obj):
#         return obj.category.get_category_display()

#     def collection(self, obj):
#         return obj.category.get_collection_display()

#     def primary_stone(self, obj):
#         return obj.category.get_primary_stone_display()

#     def obj_description(self, obj):
#         return obj.description.description
