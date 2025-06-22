import type { InventoryItem, ProductItemType } from '../../../../../types/Products';

export type Params = {
    productId: number;
    collectionName: string;
    colorName: string;
    stoneName: string;
    metalName: string;
    inventory: InventoryItem[];
    relatedProducts: ProductItemType[];
    firstImage: string;
};
