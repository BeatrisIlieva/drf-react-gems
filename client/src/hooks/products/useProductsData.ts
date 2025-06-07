import { useCallback, useEffect, useMemo, useState } from 'react';

import { useProductList } from '../../api/productsApi';
import { useCategoryName } from './useCategoryName';
import { useFilters } from './useFilters';
import { useOrdering } from './useOrdering';
import { usePagination } from './usePagination';

import type {
    Collection,
    Color,
    FetchProductsParamsExtended,
    Metal,
    Product,
    Stone
} from '../../types/ProductList';

export const useProductsData = () => {
    const { categoryName } = useCategoryName();
    const { getProductList } = useProductList();
    const { nextPage, updatePage } = usePagination();
    const {
        colorIds,
        stoneIds,
        metalIds,
        collectionIds,
        displayFilters,
        filtersMapper,
        toggleDisplayFilters,
        updateFilterByEntity,
        resetFilters
    } = useFilters();

    const { ordering, updateOrdering, resetOrdering } = useOrdering();

    const [products, setProducts] = useState<Product[]>([]);
    const [collections, setCollections] = useState<Collection[]>([]);
    const [colors, setColors] = useState<Color[]>([]);
    const [count, setCount] = useState(0);
    const [metals, setMetals] = useState<Metal[]>([]);
    const [stones, setStones] = useState<Stone[]>([]);

    const [loading, setLoading] = useState(false);

    const loadMoreDisabled = useMemo(() => nextPage === null, [nextPage]);

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

    const loadMoreHandler = useCallback(() => {
        if (!nextPage) return;

        fetchProducts({
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
        fetchProducts
    ]);

    useEffect(() => {
        fetchProducts({
            categoryName,
            shouldUpdateFiltersByEntity: true,
            shouldResetFilters: true,
            shouldResetOrdering: true
        });
    }, [categoryName, fetchProducts]);

    useEffect(() => {
        fetchProducts({
            categoryName,
            colorIds,
            stoneIds,
            metalIds,
            collectionIds,
            ordering,
            shouldUpdateFiltersByEntity: true
        });
    }, [
        categoryName,
        colorIds,
        stoneIds,
        metalIds,
        collectionIds,
        ordering,
        fetchProducts
    ]);

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
        ordering
    };
};
