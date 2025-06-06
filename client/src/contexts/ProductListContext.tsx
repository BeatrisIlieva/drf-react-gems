import { createContext, useContext } from 'react';

import type { Collection, Color, Metal, Product, Stone } from '../types/ProductList';

interface ProductListContextType {
    products: Product[];
    collections: Collection[];
    colors: Color[];
    count: number;
    metals: Metal[];
    stones: Stone[];
    loading: boolean;
    loadMoreHandler: () => void;
    loadMoreDisabled: boolean;
    updateEntityCharacteristics: (
        entityName: 'Collection' | 'Color' | 'Metal' | 'Stone',
        entityId: number
    ) => void;
    filtersMapper: {
        Color: number[];
        Stone: number[];
        Metal: number[];
        Collection: number[];
    };
    toggleDisplayFilters: () => void;
    displayFilters: boolean;
    updateOrdering: (criteria: string) => void;
    ordering: string | null;
}

export const ProductListContext = createContext<ProductListContextType>({
    products: [],
    collections: [],
    colors: [],
    count: 0,
    metals: [],
    stones: [],
    loading: false,
    loadMoreHandler: () => null,
    loadMoreDisabled: false,
    updateEntityCharacteristics: () => null,
    filtersMapper: {
        Color: [],
        Stone: [],
        Metal: [],
        Collection: []
    },
    toggleDisplayFilters: () => null,
    displayFilters: false,
    updateOrdering: () => null,
    ordering: null
});

export const useProductListContext = () => {
    const data = useContext(ProductListContext);

    return data;
};
