import { useCallback } from 'react';

const baseUrl = 'http://localhost:8000/products';

export const useCategories = () => {
    const getCategories = useCallback(async () => {
        try {
            const response = await fetch(`${baseUrl}/categories/`);
            const result = await response.json();
            console.log(result);
            return result;
        } catch (err) {
            console.log(err.message);
        }
    }, []);

    return {
        getCategories
    };
};
