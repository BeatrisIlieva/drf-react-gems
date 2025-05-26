import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';

const baseUrl = 'http://localhost:8000/products';

export const useProducts = () => {
    const { get } = useApi();

    const getProducts = useCallback(
        async ({
            categoryName,
            pageNumber = null,
            colorIds = [],
            stoneIds = [],
            materialIds = [],
            collectionIds = [],
            categoryIds = [],
            prices = []
        }) => {
            const params = new URLSearchParams();

            if (pageNumber) params.append('page', pageNumber);
            if (colorIds) {
                colorIds.forEach((id) => params.append('color_ids', id));
            }
            if (stoneIds) {
                stoneIds.forEach((id) => params.append('stone_ids', id));
            }
            if (materialIds) {
                materialIds.forEach((id) => params.append('material_ids', id));
            }
            if (collectionIds) {
                collectionIds.forEach((id) => params.append('collection_ids', id));
            }
            if (categoryIds) {
                categoryIds.forEach((id) => params.append('category_ids', id));
            }
            if (prices) {
                prices.forEach((price) => {
                    const prices = price.split(' - ');
                    const [min_price, max_price] = prices.map((x) => x.slice(1));

                    params.append('min_price', min_price);
                    params.append('max_price', max_price);
                });
            }

            const fullUrl = `${baseUrl}/${categoryName}s/?${params.toString()}`;

            try {
                const response = await get(fullUrl);
                return response;
            } catch (err) {
                console.error('Error in getProducts:', err.message);
                throw err;
            }
        },
        [get]
    );

    return { getProducts };
};

export const useProduct = () => {
    const { get } = useApi();

    const getProduct = useCallback(
        async ({ categoryName, productId }) => {
            const fullUrl = `${baseUrl}/${categoryName}s/${productId}`;

            try {
                const response = await get(fullUrl);

                return response;
            } catch (err) {
                console.error('Error in getProduct:', err.message);
                throw err;
            }
        },
        [get]
    );

    return { getProduct };
};
