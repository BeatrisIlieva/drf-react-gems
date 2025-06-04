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
        entityName: 'Collection' | 'Color' | 'Metal' | 'Price' | 'Stone',
        entityId: number | string
    ) => void;
    entityStateMapper: {
        Color: number[];
        Stone: number[];
        Metal: number[];
        Collection: number[];
        Price: string[];
    };
    toggleDisplayFilters: () => void;
    displayFilters: boolean;
    updateOrderingCriteria: (criteria: string) => void;
    orderingCriteria: string;
}

export const ProductListContext = createContext<ProductListContextType>({
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
    entityStateMapper: {
        Color: [],
        Stone: [],
        Metal: [],
        Collection: [],
        Price: []
    },
    toggleDisplayFilters: () => null,
    displayFilters: false,
    updateOrderingCriteria: () => null,
    orderingCriteria: 'rating'
});

export const useProductListContext = () => {
    const data = useContext(ProductListContext);

    return data;
};
