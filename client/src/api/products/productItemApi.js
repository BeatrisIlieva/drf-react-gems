import { useCallback } from 'react';
import { useApi } from '../../hooks/useApi';
import { keysToCamelCase } from '../../utils/convertToCamelCase';

import { HOST } from '../../constants/host';

const baseUrl = `${HOST}/api/products`;

export const useProductItem = () => {
    const { get } = useApi();

    const getProductItem = useCallback(
        async ({ categoryName, productId }) => {
            const fullUrl = `${baseUrl}/${categoryName}/${productId}`;

            try {
                const response = await get(fullUrl);

                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
            }
        },
        [get]
    );

    return { getProductItem };
};
