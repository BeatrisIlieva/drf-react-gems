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
            if (prices) {
                prices.forEach((price) => params.append('prices', price));
            }

            const fullUrl = `${baseUrl}/${categoryName}/?${params.toString()}`;

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
