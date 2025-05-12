from src.products.mixins import CaseInsensitiveUniqueNameFieldMixin, NameFieldMixin


class Reference(NameFieldMixin, CaseInsensitiveUniqueNameFieldMixin):
    pass
