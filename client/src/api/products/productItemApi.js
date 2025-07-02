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
            } catch (err) {
                if (err instanceof Error) {
                    console.error(
                        'Error in getProducts:',
                        err.message
                    );
                    throw err;
                }
                throw new Error('Unknown error in getProducts');
            }
        },
        [get]
    );

    return { getProductItem };
};
