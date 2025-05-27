from src.products.serializers import EarwearSerializer, FingerwearSerializer, NeckwearSerializer, WristwearSerializer
from src.products.models.earwear import Earwear
from src.products.models.fingerwear import Fingerwear
from src.products.models.neckwear import Neckwear
from src.products.models.wristwear import Wristwear

from src.products.views.utils import create_product_item_view

EarwearItemView = create_product_item_view(Earwear, EarwearSerializer)

FingerwearItemView = create_product_item_view(Fingerwear, FingerwearSerializer)

NeckwearItemView = create_product_item_view(Neckwear, NeckwearSerializer)

WristwearItemView = create_product_item_view(Wristwear, WristwearSerializer)
