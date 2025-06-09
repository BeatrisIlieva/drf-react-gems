import { useCallback, useEffect, useMemo, useState } from 'react';

import { useProductList } from '../../api/productsApi';
import { useCategoryName } from './useCategoryName';
import { usePagination } from './usePagination';

import type {
    Collection,
    Color,
    EntityName,
    FetchProductsParamsExtended,
    Metal,
    Product,
    Stone
} from '../../types/ProductList';
import { toggleIdInArray } from '../../utils/toggleIdInArray';

export const useProductsData = () => {
    const { categoryName } = useCategoryName();
    const { getProductList } = useProductList();
    const { nextPage, updatePage } = usePagination();

    const [products, setProducts] = useState<Product[]>([]);
    const [collections, setCollections] = useState<Collection[]>([]);
    const [colors, setColors] = useState<Color[]>([]);
    const [count, setCount] = useState(0);
    const [metals, setMetals] = useState<Metal[]>([]);
    const [stones, setStones] = useState<Stone[]>([]);
    const [colorIds, setColorIds] = useState<number[]>([]);
    const [stoneIds, setStoneIds] = useState<number[]>([]);
    const [metalIds, setMetalIds] = useState<number[]>([]);
    const [collectionIds, setCollectionIds] = useState<number[]>([]);
    const [displayFilters, setDisplayFilters] = useState(false);
    const [loading, setLoading] = useState(false);

    const [ordering, setOrdering] = useState<string | null>(null);

    const loadMoreDisabled = useMemo(() => nextPage === null, [nextPage]);

    const resetOrdering = useCallback(() => {
        setOrdering(null);
    }, []);

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
        Record<EntityName, (id: number | string) => void>
    >(
        () => ({
            Collection: (id) =>
                setCollectionIds((prev) => toggleIdInArray(prev, id as number)),
            Color: (id) => setColorIds((prev) => toggleIdInArray(prev, id as number)),
            Metal: (id) => setMetalIds((prev) => toggleIdInArray(prev, id as number)),
            Stone: (id) => setStoneIds((prev) => toggleIdInArray(prev, id as number))
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

    const fetchProducts = useCallback(
        async ({
            page,
            categoryName,
            colorIds,
            stoneIds,
            metalIds,
            collectionIds,
            ordering,
            shouldUpdateProducts = false,
            shouldUpdateFiltersByEntity = false,
            shouldResetFilters = false,
            shouldSetProductsCount = false,
            shouldResetOrdering = false
        }: FetchProductsParamsExtended) => {
            setLoading(true);

            try {
                const response = await getProductList({
                    page,
                    categoryName,
                    colorIds,
                    stoneIds,
                    metalIds,
                    collectionIds,
                    ordering
                });

                updatePage(response.next);

                if (shouldSetProductsCount) {
                    setCount(response.count);
                }

                if (shouldUpdateProducts) {
                    setProducts((prev) => [...prev, ...response.results]);
                } else {
                    setProducts(response.results);
                }

                if (shouldUpdateFiltersByEntity) {
                    setCollections(response.collections);
                    setColors(response.colors);
                    setMetals(response.metals);
                    setStones(response.stones);
                }

                if (shouldResetFilters) {
                    resetFilters();
                }

                if (shouldResetOrdering) {
                    resetOrdering();
                }
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        },
        [getProductList, updatePage, resetFilters, resetOrdering]
    );

    const updateFilterByEntity = useCallback(
        (entityName: EntityName, entityId: number | string) => {
            const toggle = toggleIdInArray;

            const newColorIds =
                entityName === 'Color' ? toggle(colorIds, entityId as number) : colorIds;
            const newStoneIds =
                entityName === 'Stone' ? toggle(stoneIds, entityId as number) : stoneIds;
            const newMetalIds =
                entityName === 'Metal' ? toggle(metalIds, entityId as number) : metalIds;
            const newCollectionIds =
                entityName === 'Collection'
                    ? toggle(collectionIds, entityId as number)
                    : collectionIds;

            filterToggleFunctions[entityName](entityId);

            fetchProducts({
                categoryName,
                colorIds: newColorIds,
                stoneIds: newStoneIds,
                metalIds: newMetalIds,
                collectionIds: newCollectionIds,
                ordering,
                shouldUpdateFiltersByEntity: true
            });
        },
        [
            colorIds,
            stoneIds,
            metalIds,
            collectionIds,
            ordering,
            fetchProducts,
            categoryName,
            filterToggleFunctions
        ]
    );

    const updateOrdering = useCallback(
        (criteria: string) => {
            setOrdering(criteria);

            fetchProducts({
                categoryName,
                colorIds,
                stoneIds,
                metalIds,
                collectionIds,
                ordering: criteria,
                shouldUpdateFiltersByEntity: true
            });
        },
        [categoryName, colorIds, stoneIds, metalIds, collectionIds, fetchProducts]
    );

    const loadMoreHandler = useCallback(async () => {
        if (!nextPage || loading || loadMoreDisabled) return;

        await fetchProducts({
            page: nextPage,
            categoryName,
            colorIds,
            stoneIds,
            metalIds,
            collectionIds,
            ordering,
            shouldUpdateProducts: true
        });

    }, [
        nextPage,
        categoryName,
        colorIds,
        stoneIds,
        metalIds,
        collectionIds,
        ordering,
        fetchProducts,
        loading,
        loadMoreDisabled
    ]);

    useEffect(() => {
        setProducts([]);
        fetchProducts({
            categoryName,
            shouldUpdateFiltersByEntity: true,
            shouldResetFilters: true,
            shouldResetOrdering: true
        });
    }, [categoryName, fetchProducts]);

    return {
        products,
        collections,
        colors,
        count,
        metals,
        stones,
        loading,
        loadMoreHandler,
        loadMoreDisabled,
        updateFilterByEntity,
        filtersMapper,
        toggleDisplayFilters,
        displayFilters,
        updateOrdering,
        ordering,
        fetchProducts
    };
};
