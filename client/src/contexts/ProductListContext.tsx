import { createContext, useContext } from 'react';

import type {
    Collection,
    Color,
    FetchProductsParams,
    Metal,
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
    stones: Stone[];
    loading: boolean;
    error: string | null;
    fetchProducts: (params: FetchProductsParams) => Promise<void>;
    loadMoreHandler: () => void;
    loadMoreDisabled: boolean;
    updateEntityCharacteristics: (
        entityName: 'Collection' | 'Color' | 'Metal' | 'Price' | 'Stone',
        entityId: number
    ) => void;
    entityStateMapper: {
        Color: number[];
        Stone: number[];
        Metal: number[];
        Collection: number[];
    };
    toggleDisplayFilters: () => void;
    resetPage: () => void;

    displayFilters: boolean;
    updateOrderingCriteria: (criteria: string) => void;
    orderingCriteria: string;

    collectionIds: number[];
    colorIds: number[];
    metalIds: number[];
    stoneIds: number[];
}

export const ProductListContext = createContext<ProductListContextType>({
    products: [],
    collections: [],
    colors: [],
    count: 0,
    metals: [],
    page: 1,
    stones: [],
    loading: false,
    error: null,
    fetchProducts: async () => {},
    loadMoreHandler: () => null,
    resetPage: () => null,
    loadMoreDisabled: false,
    updateEntityCharacteristics: () => null,
    entityStateMapper: {
        Color: [],
        Stone: [],
        Metal: [],
        Collection: []
    },
    toggleDisplayFilters: () => null,
    displayFilters: false,
    updateOrderingCriteria: () => null,
    orderingCriteria: 'rating',

    collectionIds: [],
    colorIds: [],
    metalIds: [],
    stoneIds: []
});

export const useProductListContext = () => {
    const data = useContext(ProductListContext);

    return data;
};
