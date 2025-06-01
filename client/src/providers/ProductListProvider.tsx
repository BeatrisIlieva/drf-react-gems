import { useCallback, useState, type ReactNode } from 'react';
import { useProductList } from '../api/productsApi';
import type {
    FetchProductsParams,
    ProductsResponse
} from '../types/ProductList';
import { ProductListContext } from '../contexts/ProductListContext';

interface Props {
    children: ReactNode;
}

export const ProductListProvider = ({ children }: Props) => {
    const { getProductList } = useProductList();

    const [data, setData] = useState<ProductsResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchProducts = useCallback(
        async (params: FetchProductsParams) => {
            setLoading(true);
            setError(null);

            try {
                const response = await getProductList(params);

                setData(response);
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
            value={{ data, loading, error, fetchProducts }}
        >
            {children}
        </ProductListContext.Provider>
    );
};
