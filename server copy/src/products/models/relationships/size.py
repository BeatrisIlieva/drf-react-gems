from src.products.mixins import CaseInsensitiveUniqueNameFieldMixin, NameFieldMixin


class Size(NameFieldMixin, CaseInsensitiveUniqueNameFieldMixin):
    pass
