from src.products.mixins import CaseInsensitiveUniqueNameFieldMixin, NameFieldMixin


class Collection(NameFieldMixin, CaseInsensitiveUniqueNameFieldMixin):
    pass
