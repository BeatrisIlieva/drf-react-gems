import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';
import { keysToCamelCase } from '../utils/convertToCamelCase';
import type { ProductsResponse } from '../types/ProductList';

const baseUrl = 'http://localhost:8000/products';

interface GetProductsParams {
    categoryName: string;
    pageNumber?: number | null;
    colorIds?: number[];
    stoneIds?: number[];
    metalIds?: number[];
    collectionIds?: number[];
    priceIds?: string[];
}

export const useProductList = () => {
    const { get } = useApi();

    const getProductList = useCallback(
        async ({
            categoryName,
            pageNumber = null,
            colorIds = [],
            stoneIds = [],
            metalIds = [],
            collectionIds = [],
            priceIds = []
        }: GetProductsParams) => {
            const params = new URLSearchParams();

            if (pageNumber) params.append('page', pageNumber.toString());
            if (colorIds) {
                colorIds.forEach((id) => params.append('colors', id.toString()));
            }
            if (stoneIds) {
                stoneIds.forEach((id) => params.append('stones', id.toString()));
            }
            if (metalIds) {
                metalIds.forEach((id) => params.append('materials', id.toString()));
            }
            if (collectionIds) {
                collectionIds.forEach((id) => params.append('collections', id.toString()));
            }
            if (priceIds) {
                priceIds.forEach((price) => {
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
