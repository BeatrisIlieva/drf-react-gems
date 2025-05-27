import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';

const baseUrl = 'http://localhost:8000/shopping-bag/';

export const useShoppingBag = () => {
    const { post } = useApi();

    const addToBag = useCallback(
        async ({ contentType, objectId, quantity }) => {
            const data = {
                content_type: contentType,
                object_id: objectId,
                quantity: quantity
            };

            try {
                const response = await post(baseUrl, {
                    data,
                    accessRequired: true,
                    refreshRequired: true
                });

                return response;
            } catch (err) {
                console.error('Error in addToBag:', err.message);
                throw err;
            }
        },
        [post]
    );

    return { addToBag };
};
