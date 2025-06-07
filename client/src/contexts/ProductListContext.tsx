import { createContext, useContext } from 'react';

import type {
    Collection,
    Color,
    EntityName,
    Metal,
    Product,
    Stone
} from '../types/ProductList';

interface ProductListContextType {
    count: number;
    ordering: string | null;
    loading: boolean;
    loadMoreDisabled: boolean;
    displayFilters: boolean;
    products: Product[];
    collections: Collection[];
    colors: Color[];
    metals: Metal[];
    stones: Stone[];
    filtersMapper: {
        Color: number[];
        Stone: number[];
        Metal: number[];
        Collection: number[];
    };
    loadMoreHandler: () => void;
    toggleDisplayFilters: () => void;
    updateOrdering: (criteria: string) => void;
    updateFilterByEntity: (entityName: EntityName, entityId: number) => void;
}

export const ProductListContext = createContext<ProductListContextType>({
    count: 0,
    ordering: null,
    loading: false,
    loadMoreDisabled: false,
    displayFilters: false,

    products: [],
    collections: [],
    colors: [],
    metals: [],
    stones: [],
    filtersMapper: {
        Color: [],
        Stone: [],
        Metal: [],
        Collection: []
    },
    loadMoreHandler: () => null,
    toggleDisplayFilters: () => null,
    updateOrdering: () => null,
    updateFilterByEntity: () => null
});

export const useProductListContext = () => {
    const data = useContext(ProductListContext);

    return data;
};
