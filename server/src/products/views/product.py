from src.products.models import Earwear, Neckwear, Wristwear, Fingerwear
from src.products.views.base import BaseProductListView


class EarwearListView(BaseProductListView):
    model = Earwear


class NeckwearListView(BaseProductListView):
    model = Neckwear


class WristwearListView(BaseProductListView):
    model = Wristwear


class FingerwearListView(BaseProductListView):
    model = Fingerwear
