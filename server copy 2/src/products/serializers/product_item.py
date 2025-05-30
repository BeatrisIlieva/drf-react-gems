from src.products.models.earwear import Earwear, EarwearInventory
from src.products.models.fingerwear import Fingerwear, FingerwearInventory
from src.products.models.neckwear import Neckwear, NeckwearInventory
from src.products.models.wristwear import Wristwear, WristwearInventory
from src.products.serializers.inventory import SimpleInventorySerializer, SizedInventorySerializer
from src.products.serializers.utils import create_product_item_serializer


FingerwearSerializer = create_product_item_serializer(
    model_class=Fingerwear,
    inventory_model_class=FingerwearInventory,
    inventory_serializer_base=SizedInventorySerializer,
    many=True
)

EarwearSerializer = create_product_item_serializer(
    model_class=Earwear,
    inventory_model_class=EarwearInventory,
    inventory_serializer_base=SimpleInventorySerializer,
    many=False
)

NeckwearSerializer = create_product_item_serializer(
    model_class=Neckwear,
    inventory_model_class=NeckwearInventory,
    inventory_serializer_base=SizedInventorySerializer,
    many=True
)

WristwearSerializer = create_product_item_serializer(
    model_class=Wristwear,
    inventory_model_class=WristwearInventory,
    inventory_serializer_base=SizedInventorySerializer,
    many=True
)
