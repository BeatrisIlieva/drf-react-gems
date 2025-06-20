

from src.products.models.types import Earwear, Fingerwear, Wristwear, Neckwear

from src.products.views.base import BaseProductListView


class EarwearListView(BaseProductListView):
    model = Earwear


class NeckwearListView(BaseProductListView):
    model = Neckwear


class WristwearListView(BaseProductListView):
    model = Wristwear


class FingerwearListView(BaseProductListView):
    model = Fingerwear
