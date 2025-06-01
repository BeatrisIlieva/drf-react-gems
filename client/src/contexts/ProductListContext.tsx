import { createContext, useContext } from 'react';
import type {
    Collection,
    Color,
    Metal,
    PriceRange,
    Product,
    Stone
} from '../types/ProductList';

interface ProductListContextType {
    products: Product[];
    collections: Collection[];
    colors: Color[];
    count: number;
    metals: Metal[];
    page: number;
    prices: PriceRange[];
    stones: Stone[];
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
        products: [],
        collections: [],
        colors: [],
        count: 0,
        metals: [],
        page: 1,
        prices: [],
        stones: [],
        loading: false,
        error: null,
        fetchProducts: async () => {}
    });

export const useProductListContext = () => {
    const data = useContext(ProductListContext);

    return data;
};
