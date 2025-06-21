import {
    useCallback,
    useEffect,
    useMemo,
    useState,
    type ReactNode
} from 'react';
import { ProductFiltersContext } from '../contexts/ProductFiltersContext';

import { toggleIdInArray } from '../utils/toggleIdInArray';
import { useFilters } from '../api/filtersApi';
import { useCategoryName } from '../hooks/products/useCategoryName';
import type {
    Collection,
    Color,
    EntityName,
    Metal,
    Stone
} from '../types/ProductFilters';

interface Props {
    children: ReactNode;
}

export const ProductFiltersProvider = ({ children }: Props) => {
    const { categoryName } = useCategoryName();
    const { getFilters } = useFilters();
    const [collections, setCollections] = useState<Collection[]>([]);
    const [colors, setColors] = useState<Color[]>([]);
    const [metals, setMetals] = useState<Metal[]>([]);
    const [stones, setStones] = useState<Stone[]>([]);
    const [colorIds, setColorIds] = useState<number[]>([]);
    const [stoneIds, setStoneIds] = useState<number[]>([]);
    const [metalIds, setMetalIds] = useState<number[]>([]);
    const [collectionIds, setCollectionIds] = useState<number[]>([]);
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

    const filterToggleFunctions = useMemo<
        Record<EntityName, (id: number) => void>
    >(
        () => ({
            Collection: (id) =>
                setCollectionIds((prev) => toggleIdInArray(prev, id)),
            Color: (id) => setColorIds((prev) => toggleIdInArray(prev, id)),
            Metal: (id) => setMetalIds((prev) => toggleIdInArray(prev, id)),
            Stone: (id) => setStoneIds((prev) => toggleIdInArray(prev, id))
        }),
        []
    );

    const resetFilters = useCallback(() => {
        setColorIds([]);
        setStoneIds([]);
        setMetalIds([]);
        setCollectionIds([]);
    }, []);

    const toggleDisplayFilters = useCallback(() => {
        setDisplayFilters((prev) => !prev);
    }, []);

    const fetchCollections = useCallback(async () => {
        try {
            const response = await getFilters({
                categoryName,
                entityName: 'collections',
                colorIds,
                stoneIds,
                metalIds,
                collectionIds
            });
            setCollections(response.results as Collection[]);
        } catch (error) {
            console.error(error);
        }
    }, [getFilters, categoryName, colorIds, stoneIds, metalIds, collectionIds]);

    const fetchColors = useCallback(async () => {
        try {
            const response = await getFilters({
                categoryName,
                entityName: 'colors',
                colorIds,
                stoneIds,
                metalIds,
                collectionIds
            });
            setColors(response.results as Color[]);
        } catch (error) {
            console.error(error);
        }
    }, [getFilters, categoryName, colorIds, stoneIds, metalIds, collectionIds]);

    const fetchMetals = useCallback(async () => {
        try {
            const response = await getFilters({
                categoryName,
                entityName: 'metals',
                colorIds,
                stoneIds,
                metalIds,
                collectionIds
            });
            setMetals(response.results as Metal[]);
        } catch (error) {
            console.error(error);
        }
    }, [getFilters, categoryName, colorIds, stoneIds, metalIds, collectionIds]);

    const fetchStones = useCallback(async () => {
        try {
            const response = await getFilters({
                categoryName,
                entityName: 'stones',
                colorIds,
                stoneIds,
                metalIds,
                collectionIds
            });
            setStones(response.results as Stone[]);
        } catch (error) {
            console.error(error);
        }
    }, [getFilters, categoryName, colorIds, stoneIds, metalIds, collectionIds]);

    useEffect(() => {
        fetchCollections();
        fetchColors();
        fetchMetals();
        fetchStones();
    }, [fetchCollections, fetchColors, fetchMetals, fetchStones, categoryName]);

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
