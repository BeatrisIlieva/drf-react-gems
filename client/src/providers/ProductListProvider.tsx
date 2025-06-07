// import { useCallback, useEffect, useState, type ReactNode, useMemo } from 'react';

// import { ProductListContext } from '../contexts/ProductListContext';
// import { useCategoryName } from '../hooks/useCategoryName';
// import { useProductList } from '../api/productsApi';

// import { getNextPageNumber } from '../utils/getNextPageNumber';
// import { toggleIdInArray } from '../utils/toggleIdInArray';

// import {
//     type Collection,
//     type Color,
//     type Metal,
//     type Product,
//     type Stone,
//     type EntityName,
//     type FetchProductsParamsExtended
// } from '../types/ProductList';

// interface Props {
//     children: ReactNode;
// }

// export const ProductListProvider = ({ children }: Props) => {
//     const { categoryName } = useCategoryName();
//     const { getProductList } = useProductList();

//     // State declarations
//     const [products, setProducts] = useState<Product[]>([]);
//     const [collections, setCollections] = useState<Collection[]>([]);
//     const [colors, setColors] = useState<Color[]>([]);
//     const [count, setCount] = useState(0);
//     const [metals, setMetals] = useState<Metal[]>([]);
//     const [stones, setStones] = useState<Stone[]>([]);
//     const [colorIds, setColorIds] = useState<number[]>([]);
//     const [stoneIds, setStoneIds] = useState<number[]>([]);
//     const [metalIds, setMetalIds] = useState<number[]>([]);
//     const [collectionIds, setCollectionIds] = useState<number[]>([]);
//     const [ordering, setOrdering] = useState<string | null>(null);
//     const [loading, setLoading] = useState(false);
//     const [nextPage, setNextPage] = useState<number | null>(null);
//     const [displayFilters, setDisplayFilters] = useState(false);

//     // Derived state for loadMoreDisabled to avoid an extra state variable
//     const loadMoreDisabled = useMemo(() => nextPage === null, [nextPage]);

//     // Memoized filtersMapper to avoid re-creating the object every render
//     const filtersMapper = useMemo(
//         () => ({
//             Color: colorIds,
//             Stone: stoneIds,
//             Metal: metalIds,
//             Collection: collectionIds
//         }),
//         [colorIds, stoneIds, metalIds, collectionIds]
//     );

//     // Toggle filters panel visibility
//     const toggleDisplayFilters = useCallback(() => {
//         setDisplayFilters((prev) => !prev);
//     }, []);

//     // Update ordering criteria
//     const updateOrdering = useCallback((criteria: string) => {
//         setOrdering(criteria);
//     }, []);

//     // Toggle ID in filters
//     const filterToggleFunctions = useMemo<
//         Record<EntityName, (id: number | string) => void>
//     >(
//         () => ({
//             Collection: (id) =>
//                 setCollectionIds((prev) => toggleIdInArray(prev, id as number)),
//             Color: (id) => setColorIds((prev) => toggleIdInArray(prev, id as number)),
//             Metal: (id) => setMetalIds((prev) => toggleIdInArray(prev, id as number)),
//             Stone: (id) => setStoneIds((prev) => toggleIdInArray(prev, id as number))
//         }),
//         []
//     );

//     // Updates a filter based on entity name
//     const updateFilterByEntity = useCallback(
//         (entityName: EntityName, entityId: number | string) => {
//             filterToggleFunctions[entityName](entityId);
//         },
//         [filterToggleFunctions]
//     );

//     // Update pagination state and load more disabling status
//     const updatePage = useCallback((next: string | null) => {
//         const pageNumber = getNextPageNumber(next);
//         setNextPage(pageNumber);
//     }, []);

//     // Fetch products with parameters
//     const fetchProducts = useCallback(
//         async ({
//             page,
//             categoryName,
//             colorIds,
//             stoneIds,
//             metalIds,
//             collectionIds,
//             ordering,
//             shouldUpdateProducts = false,
//             shouldUpdateFiltersByEntity = false,
//             shouldResetFilters = false,
//             shouldSetProductsCount = false
//         }: FetchProductsParamsExtended) => {
//             setLoading(true);

//             try {
//                 const response = await getProductList({
//                     page,
//                     categoryName,
//                     colorIds,
//                     stoneIds,
//                     metalIds,
//                     collectionIds,
//                     ordering
//                 });

//                 updatePage(response.next);

//                 if (shouldSetProductsCount) {
//                     setCount(response.count);
//                 }

//                 if (shouldUpdateProducts) {
//                     setProducts((prev) => [...prev, ...response.results]);
//                 } else {
//                     setProducts(response.results);
//                 }

//                 if (shouldUpdateFiltersByEntity) {
//                     setCollections(response.collections);
//                     setColors(response.colors);
//                     setMetals(response.metals);
//                     setStones(response.stones);
//                 }

//                 if (shouldResetFilters) {
//                     setColorIds([]);
//                     setStoneIds([]);
//                     setMetalIds([]);
//                     setCollectionIds([]);
//                     setDisplayFilters(false);
//                     setOrdering(null);
//                 }
//             } catch (error) {
//                 console.error(error);
//             } finally {
//                 setLoading(false);
//             }
//         },
//         [getProductList, updatePage]
//     );

//     // Load more products handler
//     const loadMoreHandler = useCallback(() => {
//         if (!nextPage) return;

//         fetchProducts({
//             page: nextPage,
//             categoryName,
//             colorIds,
//             stoneIds,
//             metalIds,
//             collectionIds,
//             ordering,
//             shouldUpdateProducts: true
//         });
//     }, [
//         nextPage,
//         categoryName,
//         colorIds,
//         stoneIds,
//         metalIds,
//         collectionIds,
//         ordering,
//         fetchProducts
//     ]);

//     // Initial load & reset when categoryName changes
//     useEffect(() => {
//         fetchProducts({
//             categoryName,
//             shouldUpdateFiltersByEntity: true,
//             shouldResetFilters: true
//         });
//     }, [categoryName, fetchProducts]);

//     // Refetch products when filters or ordering change
//     useEffect(() => {
//         fetchProducts({
//             categoryName,
//             colorIds,
//             stoneIds,
//             metalIds,
//             collectionIds,
//             ordering,
//             shouldUpdateFiltersByEntity: true
//         });
//     }, [
//         categoryName,
//         colorIds,
//         stoneIds,
//         metalIds,
//         collectionIds,
//         ordering,
//         fetchProducts
//     ]);

//     const contextValue = useMemo(
//         () => ({
//             products,
//             collections,
//             colors,
//             count,
//             metals,
//             stones,
//             loading,
//             loadMoreHandler,
//             loadMoreDisabled,
//             updateFilterByEntity,
//             filtersMapper,
//             toggleDisplayFilters,
//             displayFilters,
//             updateOrdering,
//             ordering
//         }),
//         [
//             products,
//             collections,
//             colors,
//             count,
//             metals,
//             stones,
//             loading,
//             loadMoreHandler,
//             loadMoreDisabled,
//             updateFilterByEntity,
//             filtersMapper,
//             toggleDisplayFilters,
//             displayFilters,
//             updateOrdering,
//             ordering
//         ]
//     );

//     return (
//         <ProductListContext.Provider value={contextValue}>
//             {children}
//         </ProductListContext.Provider>
//     );
// };

import { useCallback, useEffect, useState, type ReactNode, useMemo } from 'react';

import { ProductListContext } from '../contexts/ProductListContext';
import { useCategoryName } from '../hooks/useCategoryName';
import { useProductList } from '../api/productsApi';

import { getNextPageNumber } from '../utils/getNextPageNumber';

import {
    type Collection,
    type Color,
    type Metal,
    type Product,
    type Stone,
    type FetchProductsParamsExtended
} from '../types/ProductList';
import { useFilters } from '../hooks/useFilters';

interface Props {
    children: ReactNode;
}

export const ProductListProvider = ({ children }: Props) => {
    const { categoryName } = useCategoryName();
    const { getProductList } = useProductList();
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

    // State declarations
    const [products, setProducts] = useState<Product[]>([]);
    const [collections, setCollections] = useState<Collection[]>([]);
    const [colors, setColors] = useState<Color[]>([]);
    const [count, setCount] = useState(0);
    const [metals, setMetals] = useState<Metal[]>([]);
    const [stones, setStones] = useState<Stone[]>([]);

    const [ordering, setOrdering] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [nextPage, setNextPage] = useState<number | null>(null);

    // Derived state for loadMoreDisabled to avoid an extra state variable
    const loadMoreDisabled = useMemo(() => nextPage === null, [nextPage]);

    // Update ordering criteria
    const updateOrdering = useCallback((criteria: string) => {
        setOrdering(criteria);
    }, []);

    // Update pagination state and load more disabling status
    const updatePage = useCallback((next: string | null) => {
        const pageNumber = getNextPageNumber(next);
        setNextPage(pageNumber);
    }, []);

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
            shouldSetProductsCount = false
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
                    setOrdering(null);
                }
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        },
        [getProductList, updatePage, resetFilters]
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
            shouldResetFilters: true
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
