import { useCallback } from 'react';

const baseUrl = 'http://localhost:8000/products';

export const useCategories = () => {
    const getCategories = useCallback(async () => {
        try {
            const response = await fetch(`${baseUrl}/categories/`);

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            return await response.json();
        } catch (err) {
            console.error('Error in getCategories:', err.message);
            throw err; 
        }
    }, []);

    return { getCategories };
};
