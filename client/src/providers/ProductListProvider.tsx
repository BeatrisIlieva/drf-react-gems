import {
    useCallback,
    useEffect,
    useState,
    type ReactNode
} from 'react';
import { useProductList } from '../api/productsApi';
import {
    type Collection,
    type Color,
    type Metal,
    type PriceRange,
    type Product,
    type Stone,
    type ProductsResponse
} from '../types/ProductList';
import { ProductListContext } from '../contexts/ProductListContext';
import { useCategoryName } from '../hooks/useCategoryName';

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
    const [page, setPage] = useState<number>(1);
    const [prices, setPrices] = useState<PriceRange[]>([]);
    const [stones, setStones] = useState<Stone[]>([]);

    const [colorIds, setColorIds] = useState<number[]>([]);
    const [stoneIds, setStoneIds] = useState<number[]>([]);
    const [metalIds, setMetalIds] = useState<number[]>([]);
    const [collectionIds, setCollectionIds] = useState<number[]>([]);
    const [priceIds, setPriceIds] = useState<string[]>([]);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const [displayFilters, setDisplayFilters] =
        useState<boolean>(false);

    const toggleDisplayFilters = () => {
        setDisplayFilters(() => !displayFilters);
    };

    const [loadMoreDisabled, setLoadMoreDisabled] =
        useState<boolean>(false);

    const fetchProducts = useCallback(async () => {
        setLoading(true);
        setError(null);
        if (categoryName) {
            try {
                const response: ProductsResponse =
                    await getProductList({
                        categoryName,
                        pageNumber: page,
                        colorIds,
                        stoneIds,
                        metalIds,
                        collectionIds,
                        priceIds
                    });

                if (page > 1) {
                    setProducts((prev) => [
                        ...prev,
                        ...response.results
                    ]);
                } else {
                    setProducts(response.results);
                }

                setCollections(response.collections);

                setColors(response.colors);

                setMetals(response.metals);

                setPrices(response.prices);

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
    }, [
        getProductList,
        page,
        categoryName,
        colorIds,
        setPrices,
        collectionIds,
        metalIds,
        priceIds,
        stoneIds
    ]);

    const loadMoreHandler = (): void => {
        if (count <= products.length) {
            setLoadMoreDisabled(true);
            return;
        }

        const nextPage = page + 1;
        setPage(nextPage);
    };

    type EntityName =
        | 'collection'
        | 'color'
        | 'metal'
        | 'stone'
        | 'price';

    const entityMapper: Record<
        EntityName,
        (id: number | string) => void
    > = {
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
            ),
        price: (id) =>
            setPriceIds((prev) =>
                prev.includes(id as string)
                    ? prev.filter((i) => i !== id)
                    : [...prev, id as string]
            )
    };

    function updateEntityCharacteristics(
        entityName:
            | 'Collection'
            | 'Color'
            | 'Metal'
            | 'Price'
            | 'Stone',
        entityId: number | string
    ): void {
        setPage(1);
        entityMapper[
            entityName.toLowerCase() as keyof typeof entityMapper
        ](entityId);
    }

    useEffect(() => {
        if (products.length > 0) {
            if (count <= products.length) {
                setLoadMoreDisabled(true);
            } else {
                setLoadMoreDisabled(false);
            }
        }
    }, [count, products.length, page]);

    const entityStateMapper = {
        Color: colorIds,
        Stone: stoneIds,
        Metal: metalIds,
        Collection: collectionIds,
        Price: priceIds
    };

    return (
        <ProductListContext.Provider
            value={{
                products,
                collections,
                colors,
                count,
                metals,
                page,
                prices,
                stones,
                loading,
                error,
                fetchProducts,
                loadMoreHandler,
                loadMoreDisabled,
                updateEntityCharacteristics,
                entityStateMapper,
                toggleDisplayFilters,
                displayFilters
            }}
        >
            {children}
        </ProductListContext.Provider>
    );
};
