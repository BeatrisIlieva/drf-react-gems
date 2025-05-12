from src.products.mixins import CaseInsensitiveUniqueNameFieldMixin, NameFieldMixin


class Material(NameFieldMixin, CaseInsensitiveUniqueNameFieldMixin):
    pass
