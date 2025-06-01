import type {
    Collection,
    Color,
    Metal,
    PriceRange,
    Stone
} from '../../../../types/ProductList';
import type { NormalizedFilterGroup } from '../../../../types/NormalizedFilter';

export const normalizeData = (
    metals: Metal[],
    prices: PriceRange[],
    colors: Color[],
    stones: Stone[],
    collections: Collection[]
): NormalizedFilterGroup[] => {
    return [
        {
            key: 'metals',
            label: 'Metal',
            data: metals.map((item) => ({
                id: item.metalId,
                label: item.metalName,
                count: item.metalCount
            }))
        },
        {
            key: 'prices',
            label: 'Price',
            data: prices.map((item) => ({
                id: item.priceRange,
                label: item.priceRange,
                count: item.count
            }))
        },
        {
            key: 'colors',
            label: 'Color',
            data: colors.map((item) => ({
                id: item.colorId,
                label: item.colorName,
                count: item.colorCount,
                hex: item.colorHexCode
            }))
        },

        {
            key: 'stones',
            label: 'Stone',
            data: stones.map((item) => ({
                id: item.stoneId,
                label: item.stoneName,
                count: item.stoneCount,
                image: item.stoneImage
            }))
        },
        {
            key: 'collections',
            label: 'Collection',
            data: collections.map((item) => ({
                id: item.collectionId,
                label: item.collectionName,
                count: item.collectionCount
            }))
        }
    ];
};
