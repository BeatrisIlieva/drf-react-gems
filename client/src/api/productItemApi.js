import { useCallback } from 'react';

import { useApi } from '../hooks/useApi';
import { useAuth } from '../hooks/useAuth';

import { keysToCamelCase } from '../utils/convertToCamelCase';

import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/products`;

export const useProductItem = () => {
    const { get } = useApi();
    const { isAuthenticated } = useAuth();

    const getProductItem = useCallback(
        async ({ categoryName, productId }) => {
            const fullUrl = `${baseUrl}/${categoryName}/${productId}`;

            try {
                const response = await get(fullUrl, {
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated,
                });

                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
            }
        },
        [get, isAuthenticated]
    );

    return { getProductItem };
};
