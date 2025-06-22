import type { ProductItemType } from '../../../../../../types/Products';

export interface Props {
    relatedProducts: ProductItemType[];
    collectionName: string;
    productId: number;
}
