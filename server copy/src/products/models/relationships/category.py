from src.products.mixins import CaseInsensitiveUniqueNameFieldMixin, NameFieldMixin


class Category(NameFieldMixin, CaseInsensitiveUniqueNameFieldMixin):

    class Meta:
        verbose_name_plural = 'Categories'
