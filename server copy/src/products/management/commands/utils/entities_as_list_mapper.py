from src.products.models.relationships.category import Category
from src.products.models import Collection
from src.products.models import Material
from src.products.models import Reference
from src.products.models import Size


entities_as_list_mapper = {
    Category: [
        'Wristwear',
        'Earwear',
        'Neckwear',
        'Fingerwear'
    ],
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
        'Watch',
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
        'Classics',
        'Elegant',
    ],
    Size: [
        'XS',
        'S',
        'M',
        'L',
        'XL',
        'One Size',
    ]
}
