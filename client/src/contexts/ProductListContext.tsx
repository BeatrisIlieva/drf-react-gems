import { createContext, useContext } from 'react';

import type { Product } from '../types/ProductList';

interface ProductListContextType {
    count: number;
    ordering: string | null;
    loading: boolean;
    loadMoreDisabled: boolean;
    products: Product[];
    loadMoreHandler: () => void;
    updateOrdering: (criteria: string) => void;
}

export const ProductListContext = createContext<ProductListContextType>({
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
