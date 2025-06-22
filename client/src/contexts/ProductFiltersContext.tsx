import { createContext, useContext } from 'react';
import type {
    Collection,
    Color,
    EntityName,
    Metal,
    Stone
} from '../types/Products';

interface ProductFiltersContextType {
    displayFilters: boolean;
    collections: Collection[];
    colors: Color[];
    metals: Metal[];
    stones: Stone[];
    collectionIds: number[];
    colorIds: number[];
    metalIds: number[];
    stoneIds: number[];
    filtersMapper: {
        Color: number[];
        Stone: number[];
        Metal: number[];
        Collection: number[];
    };
    toggleDisplayFilters: () => void;
    filterToggleFunctions: Record<
        EntityName,
        (id: number) => void
    >;
}

export const ProductFiltersContext =
    createContext<ProductFiltersContextType>({
        collections: [],
        colors: [],
        metals: [],
        stones: [],
        colorIds: [],
        stoneIds: [],
        metalIds: [],
        collectionIds: [],
        displayFilters: false,
        filtersMapper: {
            Color: [],
            Stone: [],
            Metal: [],
            Collection: []
        },
        toggleDisplayFilters: () => null,
        filterToggleFunctions: {
            Collection: () => null,
            Color: () => null,
            Metal: () => null,
            Stone: () => null
        }
    });

export const useProductFiltersContext = () => {
    const data = useContext(ProductFiltersContext);

    return data;
};
