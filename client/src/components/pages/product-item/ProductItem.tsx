import { useState, type ReactElement } from 'react';
import { useProductItem } from '../../../api/productItemApi';
import type { ProductItemType } from '../../../types/Products';

export const ProductItem = (): ReactElement => {
    const { getProductItem } = useProductItem();

    const [product, setProduct] = useState<ProductItemType>({})
 };
