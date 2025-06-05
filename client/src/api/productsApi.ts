import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';
import { keysToCamelCase } from '../utils/convertToCamelCase';
import type { FetchProductsParams, ProductsResponse } from '../types/ProductList';

const baseUrl = 'http://localhost:8000/products';

export const useProductList = () => {
    const { get } = useApi();

    const getProductList = useCallback(
        async ({
            categoryName,
            page = null,
            colorIds = [],
            stoneIds = [],
            metalIds = [],
            collectionIds = [],
            ordering = ''
        }: FetchProductsParams) => {
            const params = new URLSearchParams();

            if (page) params.append('page', page.toString());
            if (colorIds) {
                colorIds.forEach((id) => params.append('colors', id.toString()));
            }
            if (stoneIds) {
                stoneIds.forEach((id) => params.append('stones', id.toString()));
            }
            if (metalIds) {
                metalIds.forEach((id) => params.append('metals', id.toString()));
            }
            if (collectionIds) {
                collectionIds.forEach((id) =>
                    params.append('collections', id.toString())
                );
            }
            if (ordering) params.append('ordering', ordering);

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
