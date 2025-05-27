from src.products.models.earwear import Earwear
from src.products.models.fingerwear import Fingerwear
from src.products.models.neckwear import Neckwear
from src.products.models.wristwear import Wristwear

from src.products.views.utils import create_product_list_view

EarwearListView = create_product_list_view(Earwear)

FingerwearListView = create_product_list_view(Fingerwear)

NeckwearListView = create_product_list_view(Neckwear)

WristwearListView = create_product_list_view(Wristwear)
