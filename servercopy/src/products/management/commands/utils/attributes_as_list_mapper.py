from src.products.models import Collection, Metal, Size, Stone, Color


attributes_as_list_mapper = {
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
        'Bracelet',
        'Lilium',
        'Myosotis',
        'Drop',
    ],
    Metal: [
        'Yellow Gold',
        'Rose Gold',
        'Platinum',
    ],
    Size: [
        'Small',
        'Medium',
        'Large',
    ],
    Stone: [
        'Aquamarine',
        'Diamond',
        'Emerald',
        'Ruby',
        'Sapphire',
    ],
    Color: [
        'Blue',
        'Green',
        'Pink',
        'Red',
        'White',
        'Yellow',
    ],
}
