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

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

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
                        pageNumber: page
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
                setCount(response.count);
                setMetals(response.metals);
                setPrices(response.prices);
                setStones(response.stones);
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
    }, [getProductList, page, categoryName]);

    const loadMoreHandler = (): void => {
        if (count <= products.length) {
            setLoadMoreDisabled(true);
            return;
        }

        const nextPage = page + 1;
        setPage(nextPage);
    };

    useEffect(() => {
        if (products.length > 0 && count <= products.length) {
            setLoadMoreDisabled(true);
        }
    }, [count, products.length]);

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
                loadMoreDisabled
            }}
        >
            {children}
        </ProductListContext.Provider>
    );
};
