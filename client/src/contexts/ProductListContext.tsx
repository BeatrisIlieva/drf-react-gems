import { createContext, useContext } from 'react';

import type { ProductListType } from '../types/Products';

interface ProductListContextType {
    count: number;
    ordering: string | null;
    loading: boolean;
    loadMoreDisabled: boolean;
    products: ProductListType[];
    loadMoreHandler: () => void;
    updateOrdering: (criteria: string) => void;
}

export const ProductListContext =
    createContext<ProductListContextType>({
        count: 0,
        ordering: null,
        loading: false,
        loadMoreDisabled: false,
        products: [],
        loadMoreHandler: () => null,
        updateOrdering: () => null
    });

export const useProductListContext = () => {
    const data = useContext(ProductListContext);

    return data;
};
