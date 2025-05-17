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
        async (categoryId, pageNumber = null) => {
            const fullUrl = pageNumber
                ? `${baseUrl}/?category=${categoryId}&page=${pageNumber}`
                : `${baseUrl}/?category=${categoryId}`;
                
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
