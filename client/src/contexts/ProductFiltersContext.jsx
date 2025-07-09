import { createContext, useContext } from 'react';

export const ProductFiltersContext = createContext({
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
        Collection: [],
    },
    toggleDisplayFilters: () => null,
    filterToggleFunctions: {
        Collection: () => null,
        Color: () => null,
        Metal: () => null,
        Stone: () => null,
    },
});

export const useProductFiltersContext = () => {
    const data = useContext(ProductFiltersContext);

    return data;
};
