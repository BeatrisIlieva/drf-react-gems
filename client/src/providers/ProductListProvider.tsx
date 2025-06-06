import { useCallback, useEffect, useState, type ReactNode } from 'react';

import { ProductListContext } from '../contexts/ProductListContext';
import { useProductList } from '../api/productsApi';

import {
    type Collection,
    type Color,
    type Metal,
    type Product,
    type Stone,
    type EntityName,
    type ProductFilters
} from '../types/ProductList';
import { useCategoryName } from '../hooks/useCategoryName';
import { getNextPageNumber } from '../utils/getNextPageNumber';

interface Props {
    children: ReactNode;
}

export const ProductListProvider = ({ children }: Props) => {
    const { categoryName } = useCategoryName();
    const { getProductList } = useProductList();

    const [products, setProducts] = useState<Product[]>([]);
    const [collections, setCollections] = useState<Collection[]>([]);
    const [colors, setColors] = useState<Color[]>([]);
    const [count, setCount] = useState<number>(0);
    const [metals, setMetals] = useState<Metal[]>([]);
    const [stones, setStones] = useState<Stone[]>([]);

    const [colorIds, setColorIds] = useState<number[]>([]);
    const [stoneIds, setStoneIds] = useState<number[]>([]);
    const [metalIds, setMetalIds] = useState<number[]>([]);
    const [collectionIds, setCollectionIds] = useState<number[]>([]);

    const [ordering, setOrdering] = useState<string | null>(null);

    const [loading, setLoading] = useState(false);
    const [nextPage, setNextPage] = useState<number | null>(null);

    const [displayFilters, setDisplayFilters] = useState<boolean>(false);
    const [loadMoreDisabled, setLoadMoreDisabled] = useState<boolean>(false);

    const toggleDisplayFilters = () => {
        setDisplayFilters(() => !displayFilters);
    };

    const updateOrdering = (criteria: string) => {
        setOrdering(criteria);
    };

    const entityMapper: Record<EntityName, (id: number | string) => void> = {
        collection: (id) =>
            setCollectionIds((prev) =>
                prev.includes(id as number)
                    ? prev.filter((i) => i !== id)
                    : [...prev, id as number]
            ),
        color: (id) =>
            setColorIds((prev) =>
                prev.includes(id as number)
                    ? prev.filter((i) => i !== id)
                    : [...prev, id as number]
            ),
        metal: (id) =>
            setMetalIds((prev) =>
                prev.includes(id as number)
                    ? prev.filter((i) => i !== id)
                    : [...prev, id as number]
            ),
        stone: (id) =>
            setStoneIds((prev) =>
                prev.includes(id as number)
                    ? prev.filter((i) => i !== id)
                    : [...prev, id as number]
            )
    };

    const updateEntityCharacteristics = (
        entityName: 'Collection' | 'Color' | 'Metal' | 'Stone',
        entityId: number | string
    ): void => {
        entityMapper[entityName.toLowerCase() as keyof typeof entityMapper](entityId);
    };

    function loadMoreHandler(): void {
        setLoading(true);

        getProductList({
            page: nextPage,
            categoryName,
            colorIds,
            stoneIds,
            metalIds,
            collectionIds,
            ordering
        })
            .then((response) => {
                setProducts((prev) => [...prev, ...response.results]);

                updatePage(response.next);
            })
            .catch((err) => console.log(err.message))
            .finally(() => setLoading(false));
    }

    useEffect(() => {
        setLoading(true);

        getProductList({
            categoryName
        })
            .then((response) => {
                setProducts(response.results);

                updatePage(response.next);

                updateProductFilters({
                    collections: response.collections,
                    colors: response.colors,
                    metals: response.metals,
                    stones: response.stones
                });

                setCount(response.count);

                setColorIds([]);
                setStoneIds([]);
                setMetalIds([]);
                setCollectionIds([]);
                setDisplayFilters(false);
                setOrdering(null);
                setLoadMoreDisabled(response.count <= response.results.length);
            })
            .catch((err) => console.log(err.message))
            .finally(() => setLoading(false));
    }, [categoryName, getProductList]);

    useEffect(() => {
        setLoading(true);

        getProductList({
            categoryName,
            colorIds,
            stoneIds,
            metalIds,
            collectionIds,
            ordering
        })
            .then((response) => {
                setProducts(response.results);

                updatePage(response.next);

                updateProductFilters({
                    collections: response.collections,
                    colors: response.colors,
                    metals: response.metals,
                    stones: response.stones
                });
            })
            .catch((err) => console.log(err.message))
            .finally(() => setLoading(false));
    }, [
        colorIds,
        stoneIds,
        metalIds,
        collectionIds,
        ordering,
        categoryName,
        getProductList
    ]);

    const updateProductFilters = ({
        collections,
        colors,
        metals,
        stones
    }: ProductFilters) => {
        setCollections(collections);
        setColors(colors);
        setMetals(metals);
        setStones(stones);
    };

    const updatePage = (next: string | null) => {
        const pageNumber = getNextPageNumber(next);
        setNextPage(pageNumber);
        setLoadMoreDisabled(pageNumber ? false : true);
    };

    const filtersMapper = {
        Color: colorIds,
        Stone: stoneIds,
        Metal: metalIds,
        Collection: collectionIds
    };

    return (
        <ProductListContext.Provider
            value={{
                products,
                collections,
                colors,
                count,
                metals,
                stones,
                loading,
                loadMoreHandler,
                loadMoreDisabled,
                updateEntityCharacteristics,
                filtersMapper,
                toggleDisplayFilters,
                displayFilters,
                updateOrdering,
                ordering
            }}
        >
            {children}
        </ProductListContext.Provider>
    );
};
