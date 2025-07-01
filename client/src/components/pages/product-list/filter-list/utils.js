const stoneNameByImage = {
    Aquamarine:
        'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748232/aquamarine_b4dtyx.webp',
    Diamond:
        'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748236/diamond_dkg8rb.webp',
    Emerald:
        'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748237/emerald_auiwk4.webp',
    Ruby: 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748233/ruby_g7idgx.webp',
    Sapphire:
        'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748233/blue-sapphire_bjwmoo.webp'
};

const colorNameByHex = {
    Blue: '#719cf0',
    Green: '#06986f',
    Pink: '#fa94ac',
    Red: '#e93e3e',
    White: '#fff',
    Yellow: '#faf098'
};

export const normalizeData = (
    metals,
    colors,
    stones,
    collections
) => {
    return [
        {
            key: 'metals',
            label: 'Metal',
            data: (metals || []).map((item) => ({
                id: item.id,
                label: item.name,
                count: item.count
            }))
        },
        {
            key: 'colors',
            label: 'Color',
            data: (colors || []).map((item) => ({
                id: item.id,
                label: item.name,
                count: item.count,
                hex: colorNameByHex[item.name]
            }))
        },
        {
            key: 'stones',
            label: 'Stone',
            data: (stones || []).map((item) => ({
                id: item.id,
                label: item.name,
                count: item.count,
                image: stoneNameByImage[item.name]
            }))
        },
        {
            key: 'collections',
            label: 'Collection',
            data: (collections || []).map((item) => ({
                id: item.id,
                label: item.name,
                count: item.count
            }))
        }
    ];
};
