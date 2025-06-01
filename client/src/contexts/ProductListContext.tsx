import { createContext, useContext } from 'react';
import type { ProductsResponse } from '../types/ProductList';

interface ProductListContextType {
    data: ProductsResponse | null;
    loading: boolean;
    error: string | null;
    fetchProducts: (params: {
        categoryName: string;
        pageNumber?: string | null;
        colorIds?: string[];
        stoneIds?: string[];
        materialIds?: string[];
        collectionIds?: string[];
        prices?: string[];
    }) => Promise<void>;
}

export const ProductListContext =
    createContext<ProductListContextType>({
        data: null,
        loading: false,
        error: null,
        fetchProducts: async () => {}
    });

export const useProductListContext = () => {
    const data = useContext(ProductListContext);

    return data;
};
