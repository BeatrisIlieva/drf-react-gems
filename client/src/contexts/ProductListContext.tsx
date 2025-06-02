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
    fetchProducts: () => Promise<void>;
    loadMoreHandler: () => void;
    loadMoreDisabled: boolean;
    updateEntityCharacteristics: (
        entityName:
            | 'Collection'
            | 'Color'
            | 'Metal'
            | 'Price'
            | 'Stone',
        entityId: number | string
    ) => void;
    entityStateMapper: any;
}

// params: {
//     colorIds?: string[];
//     stoneIds?: string[];
//     materialIds?: string[];
//     collectionIds?: string[];
//     prices?: string[];
// }

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
        fetchProducts: async () => {},
        loadMoreHandler: () => null,
        loadMoreDisabled: false,
        updateEntityCharacteristics: () => null,
        entityStateMapper: {},
    });

export const useProductListContext = () => {
    const data = useContext(ProductListContext);

    return data;
};
