import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';

const baseUrl = 'http://localhost:8000/products';

export const useCategories = () => {
    const { get } = useApi();

    const getCategories = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/categories/`);

            return response;
        } catch (err) {
            console.error('Error in getCategories:', err.message);
            throw err;
        }
    }, [get]);

    return { getCategories };
};

export const useProducts = () => {
    const { get } = useApi();

    const getProducts = useCallback(
        async ({
            categoryId,
            pageNumber = null,
            colorIds = [],
            stoneIds = [],
            materialIds = []
        }) => {
            const params = new URLSearchParams();

            if (categoryId) params.append('category', categoryId);
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

            const fullUrl = `${baseUrl}/?${params.toString()}`;

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
