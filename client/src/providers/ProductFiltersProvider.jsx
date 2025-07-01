import { useCallback, useEffect, useMemo, useState } from 'react';
import { ProductFiltersContext } from '../contexts/ProductFiltersContext';

import { toggleIdInArray } from '../utils/toggleIdInArray';
import { useFilters } from '../api/filtersApi';
import { useCategoryName } from '../hooks/products/useCategoryName';

export const ProductFiltersProvider = ({ children }) => {
    const { categoryName } = useCategoryName();
    const { getFilters } = useFilters();
    const [collections, setCollections] = useState([]);
    const [colors, setColors] = useState([]);
    const [metals, setMetals] = useState([]);
    const [stones, setStones] = useState([]);
    const [colorIds, setColorIds] = useState([]);
    const [stoneIds, setStoneIds] = useState([]);
    const [metalIds, setMetalIds] = useState([]);
    const [collectionIds, setCollectionIds] = useState([]);
    const [displayFilters, setDisplayFilters] = useState(false);

    const filtersMapper = useMemo(
        () => ({
            Color: colorIds,
            Stone: stoneIds,
            Metal: metalIds,
            Collection: collectionIds
        }),
        [colorIds, stoneIds, metalIds, collectionIds]
    );

    const filterToggleFunctions = useMemo(
        () => ({
            Collection: (id) =>
                setCollectionIds((prev) =>
                    toggleIdInArray(prev, id)
                ),
            Color: (id) =>
                setColorIds((prev) => toggleIdInArray(prev, id)),
            Metal: (id) =>
                setMetalIds((prev) => toggleIdInArray(prev, id)),
            Stone: (id) =>
                setStoneIds((prev) => toggleIdInArray(prev, id))
        }),
        []
    );

    const resetFilters = useCallback(() => {
        setColorIds([]);
        setStoneIds([]);
        setMetalIds([]);
        setCollectionIds([]);
        setDisplayFilters(false);
    }, []);

    const toggleDisplayFilters = useCallback(() => {
        setDisplayFilters((prev) => !prev);
    }, []);

    const fetchFiltersData = useCallback(
        async (entityName) => {
            try {
                const response = await getFilters({
                    categoryName,
                    entityName: `${entityName.toLowerCase()}s`,
                    colorIds,
                    stoneIds,
                    metalIds,
                    collectionIds
                });

                return response?.results || [];
            } catch (error) {
                console.error(error);
                return [];
            }
        },
        [
            getFilters,
            categoryName,
            colorIds,
            stoneIds,
            metalIds,
            collectionIds
        ]
    );

    const fetchCollections = useCallback(async () => {
        try {
            const data = await fetchFiltersData('Collection');
            setCollections(data);
        } catch (error) {
            console.error(error);
        }
    }, [fetchFiltersData]);

    const fetchColors = useCallback(async () => {
        try {
            const data = await fetchFiltersData('Color');
            setColors(data);
        } catch (error) {
            console.error(error);
        }
    }, [fetchFiltersData]);

    const fetchMetals = useCallback(async () => {
        try {
            const data = await fetchFiltersData('Metal');
            setMetals(data);
        } catch (error) {
            console.error(error);
        }
    }, [fetchFiltersData]);

    const fetchStones = useCallback(async () => {
        try {
            const data = await fetchFiltersData('Stone');
            setStones(data);
        } catch (error) {
            console.error(error);
        }
    }, [fetchFiltersData]);

    useEffect(() => {
        fetchCollections();
        fetchColors();
        fetchMetals();
        fetchStones();
    }, [
        fetchCollections,
        fetchColors,
        fetchMetals,
        fetchStones,
        categoryName
    ]);

    const contextValue = useMemo(
        () => ({
            collections,
            colors,
            metals,
            stones,
            colorIds,
            stoneIds,
            metalIds,
            collectionIds,
            displayFilters,
            filtersMapper,
            toggleDisplayFilters,
            filterToggleFunctions
        }),
        [
            collections,
            colors,
            metals,
            stones,
            colorIds,
            stoneIds,
            metalIds,
            collectionIds,
            displayFilters,
            filtersMapper,
            toggleDisplayFilters,
            filterToggleFunctions
        ]
    );

    useEffect(() => {
        resetFilters();
    }, [categoryName, resetFilters]);

    return (
        <ProductFiltersContext.Provider value={contextValue}>
            {children}
        </ProductFiltersContext.Provider>
    );
};
