import { useCallback, useEffect, useMemo, useState } from "react";

import { ProductListContext } from "../contexts/ProductListContext";
import { useProductList } from "../api/productListApi";
import { useCategoryName } from "../hooks/useCategoryName";
import { usePagination } from "../hooks/usePagination";

import { useProductFiltersContext } from "../contexts/ProductFiltersContext";

export const ProductListProvider = ({ children }) => {
    const { categoryName } = useCategoryName();
    const { getProductList } = useProductList();
    const { nextPage, updatePage } = usePagination();
    const { colorIds, stoneIds, metalIds, collectionIds } =
        useProductFiltersContext();

    const [count, setCount] = useState(0);
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [ordering, setOrdering] = useState(null);

    const loadMoreDisabled = useMemo(() => nextPage === null, [nextPage]);

    const resetOrdering = useCallback(() => {
        setOrdering(null);
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
            shouldSetProductsCount = false,
            shouldResetOrdering = false,
        }) => {
            setLoading(true);
            setError(null);

            try {
                const response = await getProductList({
                    page,
                    categoryName,
                    colorIds,
                    stoneIds,
                    metalIds,
                    collectionIds,
                    ordering,
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

                if (shouldResetOrdering) {
                    resetOrdering();
                }
            } catch (err) {
                setError(err.message || "Failed to load products");
                if (!shouldUpdateProducts) {
                    setProducts([]);
                }
            } finally {
                setLoading(false);
            }
        },
        [getProductList, updatePage, resetOrdering],
    );

    const updateOrdering = useCallback(
        (criteria) => {
            setOrdering(criteria);

            fetchProducts({
                categoryName,
                colorIds,
                stoneIds,
                metalIds,
                collectionIds,
                ordering: criteria,
            });
        },
        [
            categoryName,
            colorIds,
            stoneIds,
            metalIds,
            collectionIds,
            fetchProducts,
            setOrdering,
        ],
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
            shouldUpdateProducts: true,
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
        loadMoreDisabled,
    ]);

    useEffect(() => {
        setProducts([]);
        fetchProducts({
            categoryName,
            shouldResetOrdering: true,
        });
    }, [categoryName, fetchProducts]);

    useEffect(() => {
        setProducts([]);
        setCount(0);
        updatePage(null);
        fetchProducts({
            categoryName,
            colorIds,
            stoneIds,
            metalIds,
            collectionIds,
            ordering,
        });
    }, [
        colorIds,
        stoneIds,
        metalIds,
        collectionIds,
        categoryName,
        fetchProducts,
        ordering,
        updatePage,
    ]);

    const contextValue = useMemo(
        () => ({
            products,
            loading,
            error,
            loadMoreHandler,
            loadMoreDisabled,
            updateOrdering,
            ordering,
            fetchProducts,
            count,
        }),
        [
            products,
            loading,
            error,
            loadMoreHandler,
            loadMoreDisabled,
            updateOrdering,
            ordering,
            fetchProducts,
            count,
        ],
    );

    return (
        <ProductListContext.Provider value={contextValue}>
            {children}
        </ProductListContext.Provider>
    );
};
