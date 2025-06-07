import { useCallback, useEffect, useState, type ReactNode, useMemo } from 'react';

import { ProductListContext } from '../contexts/ProductListContext';
import { useCategoryName } from '../hooks/useCategoryName';
import { useProductList } from '../api/productsApi';

import {
    type Collection,
    type Color,
    type Metal,
    type Product,
    type Stone,
    type FetchProductsParamsExtended
} from '../types/ProductList';
import { useFilters } from '../hooks/useFilters';
import { useOrdering } from '../hooks/useOrdering';
import { usePagination } from '../hooks/usePagination';

interface Props {
    children: ReactNode;
}

export const ProductListProvider = ({ children }: Props) => {
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

    // State declarations
    const [products, setProducts] = useState<Product[]>([]);
    const [collections, setCollections] = useState<Collection[]>([]);
    const [colors, setColors] = useState<Color[]>([]);
    const [count, setCount] = useState(0);
    const [metals, setMetals] = useState<Metal[]>([]);
    const [stones, setStones] = useState<Stone[]>([]);

    const [loading, setLoading] = useState(false);

    // Derived state for loadMoreDisabled to avoid an extra state variable
    const loadMoreDisabled = useMemo(() => nextPage === null, [nextPage]);

    // Fetch products with parameters
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

    // Load more products handler
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

    // Initial load & reset when categoryName changes
    useEffect(() => {
        fetchProducts({
            categoryName,
            shouldUpdateFiltersByEntity: true,
            shouldResetFilters: true,
            shouldResetOrdering: true
        });
    }, [categoryName, fetchProducts]);

    // Refetch products when filters or ordering change
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

    const contextValue = useMemo(
        () => ({
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
        }),
        [
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
        ]
    );

    return (
        <ProductListContext.Provider value={contextValue}>
            {children}
        </ProductListContext.Provider>
    );
};
