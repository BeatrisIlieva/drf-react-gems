from src.products.models import Collection
from src.products.models import Material
from src.products.models import Reference
from src.products.models.fingerwear import FingerwearSize
from src.products.models.neckwear import NeckwearSize
from src.products.models.wristwear import WristwearSize


entities_as_list_mapper = {
    Collection: [
        'Daisy',
        'Gerbera',
        'Forget Me Not',
        'Lily',
        'Lotus',
        'Leaf',
        'Berry',
        'Sunflower',
        'Lily of the Valley',
        'Classics',
        'Elegant',
    ],
    Material: [
        'Yellow Gold',
        'Rose Gold',
        'Platinum',
    ],
    Reference: [
        'Stud',
        'Drop',
        'Pendant',
        'Lariat',
        'Tennis',
        'Chain',
        'Watch',
        'Statement',
        'Band',
    ],
    FingerwearSize: [
        4.90,
        5.05,
        5.30,
        5.43,
        5.56,
        5.68,
    ],
    NeckwearSize: [
        40.64,
        45.72,
        50.80,
        71.28,
        91.44,
        142.88
    ],
    WristwearSize: [
        12.70,
        14.20,
        15.40,
        16.50,
        17.80,
    ]
}
