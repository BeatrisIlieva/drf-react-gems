import {
    type ReactNode,
    useCallback,
    useEffect,
    useMemo,
    useState
} from 'react';

import { ProductListContext } from '../contexts/ProductListContext';
import { useProductList } from '../api/productsApi';
import { useCategoryName } from '../hooks/products/useCategoryName';
import { usePagination } from '../hooks/products/usePagination';
import type {
    FetchProductsParamsExtended,
    Product
} from '../types/ProductList';
import { useProductFiltersContext } from '../contexts/ProductFiltersContext';

interface Props {
    children: ReactNode;
}

export const ProductListProvider = ({ children }: Props) => {
    const { categoryName } = useCategoryName();
    const { getProductList } = useProductList();
    const { nextPage, updatePage } = usePagination();
    const { colorIds, stoneIds, metalIds, collectionIds } =
        useProductFiltersContext();

    const [count, setCount] = useState(0);
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(false);
    const [ordering, setOrdering] = useState<string | null>(null);

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

                if (shouldResetOrdering) {
                    resetOrdering();
                }
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        },
        [getProductList, updatePage, resetOrdering]
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
                ordering: criteria
            });
        },
        [
            categoryName,
            colorIds,
            stoneIds,
            metalIds,
            collectionIds,
            fetchProducts
        ]
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
            ordering
        });
    }, [
        colorIds,
        stoneIds,
        metalIds,
        collectionIds,
        categoryName,
        fetchProducts,
        ordering
    ]);

    const contextValue = useMemo(
        () => ({
            products,
            loading,
            loadMoreHandler,
            loadMoreDisabled,
            updateOrdering,
            ordering,
            fetchProducts,
            count
        }),
        [
            products,
            loading,
            loadMoreHandler,
            loadMoreDisabled,
            updateOrdering,
            ordering,
            fetchProducts,
            count
        ]
    );

    return (
        <ProductListContext.Provider value={contextValue}>
            {children}
        </ProductListContext.Provider>
    );
};
