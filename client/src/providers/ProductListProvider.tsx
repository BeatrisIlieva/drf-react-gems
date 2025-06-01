import { useCallback, useState, type ReactNode } from 'react';
import { useProductList } from '../api/productsApi';
import {
    type Collection,
    type Color,
    type Metal,
    type PriceRange,
    type Product,
    type Stone,
    type FetchProductsParams,
    type ProductsResponse
} from '../types/ProductList';
import { ProductListContext } from '../contexts/ProductListContext';

interface Props {
    children: ReactNode;
}

export const ProductListProvider = ({ children }: Props) => {
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

    const fetchProducts = useCallback(
        async (params: FetchProductsParams) => {
            setLoading(true);
            setError(null);

            try {
                const response: ProductsResponse =
                    await getProductList(params);

                setProducts(response.results);
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
        },
        [getProductList]
    );

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
                fetchProducts
            }}
        >
            {children}
        </ProductListContext.Provider>
    );
};
