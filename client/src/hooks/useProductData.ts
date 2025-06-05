import { useCallback, useEffect, useState } from 'react';
import { useProductList } from '../api/productsApi';
import { useCategoryName } from './useCategoryName';
import type {
    Collection,
    Color,
    FetchProductsParams,
    Metal,
    Product,
    ProductsResponse,
    Stone
} from '../types/ProductList';

export const useProductData = () => {
    const { categoryName } = useCategoryName();
    const { getProductList } = useProductList();

    const [products, setProducts] = useState<Product[]>([]);
    const [collections, setCollections] = useState<Collection[]>([]);
    const [colors, setColors] = useState<Color[]>([]);
    const [count, setCount] = useState<number>(0);
    const [metals, setMetals] = useState<Metal[]>([]);
    const [stones, setStones] = useState<Stone[]>([]);

    const [page, setPage] = useState<number>(1);
    const [loadMoreDisabled, setLoadMoreDisabled] = useState<boolean>(false);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchProducts = useCallback(
        async ({
            colorIds,
            stoneIds,
            metalIds,
            collectionIds,
            ordering,
            page
        }: FetchProductsParams) => {
            setLoading(true);
            setError(null);

            if (categoryName) {
                try {
                    const response: ProductsResponse = await getProductList({
                        categoryName,
                        page,
                        colorIds,
                        stoneIds,
                        metalIds,
                        collectionIds,
                        ordering
                    });

                    if (page && page > 1) {
                        setProducts((prev) => [...prev, ...response.results]);
                    } else {
                        setProducts(response.results);
                    }

                    setCollections(response.collections);

                    setColors(response.colors);

                    setMetals(response.metals);

                    setStones(response.stones);

                    setCount(response.count);
                } catch (err) {
                    if (err instanceof Error) {
                        setError(err.message);
                    } else {
                        setError('Unknown error');
                    }
                } finally {
                    setLoading(false);
                }
            }
        },
        [getProductList, categoryName]
    );

    const resetPage = () => {
        setPage(() => 1);
    };

    const loadMoreHandler = (): void => {
        if (count <= products.length) {
            setLoadMoreDisabled(true);

            return;
        }

        setPage(() => page + 1);
    };

    useEffect(() => {
        resetPage();
        setLoadMoreDisabled(false);
    }, [categoryName]);

    useEffect(() => {
        if (products.length > 0) {
            if (count <= products.length) {
                setLoadMoreDisabled(true);
            } else {
                setLoadMoreDisabled(false);
            }
        }
    }, [count, products.length, page]);

    return {
        products,
        collections,
        colors,
        count,
        metals,
        stones,
        loading,
        error,
        fetchProducts,
        page,
        loadMoreDisabled,
        loadMoreHandler,
        resetPage
    };
};
