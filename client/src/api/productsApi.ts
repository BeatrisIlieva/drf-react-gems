import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';
import { keysToCamelCase } from '../utils/convertToCamelCase';
import type { ProductsResponse } from '../types/ProductList';

const baseUrl = 'http://localhost:8000/products';

interface GetProductsParams {
    categoryName: string;
    pageNumber?: number | null;
    colorIds?: string[];
    stoneIds?: string[];
    materialIds?: string[];
    collectionIds?: string[];
    prices?: string[];
}

export const useProductList = () => {
    const { get } = useApi();

    const getProductList = useCallback(
        async ({
            categoryName,
            pageNumber = null,
            colorIds = [],
            stoneIds = [],
            materialIds = [],
            collectionIds = [],
            prices = []
        }: GetProductsParams) => {
            const params = new URLSearchParams();

            if (pageNumber) params.append('page', pageNumber.toString());
            if (colorIds) {
                colorIds.forEach((id) => params.append('colors', id));
            }
            if (stoneIds) {
                stoneIds.forEach((id) => params.append('stones', id));
            }
            if (materialIds) {
                materialIds.forEach((id) => params.append('materials', id));
            }
            if (collectionIds) {
                collectionIds.forEach((id) => params.append('collections', id));
            }
            if (prices) {
                prices.forEach((price) => {
                    const [min_price, max_price] = price
                        .split(' - ')
                        .map((p) => p.slice(1));
                    params.append('prices', `${min_price}-${max_price}`);
                });
            }

            const fullUrl = `${baseUrl}/${categoryName}/?${params.toString()}`;

            try {
                const response: ProductsResponse = await get(fullUrl);

                return keysToCamelCase(response);
            } catch (err: unknown) {
                if (err instanceof Error) {
                    console.error('Error in getProducts:', err.message);
                    throw err;
                }
                throw new Error('Unknown error in getProducts');
            }
        },
        [get]
    );

    return { getProductList };
};
