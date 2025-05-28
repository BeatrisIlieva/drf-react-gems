import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';
import { useAuth } from '../hooks/useAuth';
import { useGuest } from '../hooks/useGuest';

const baseUrl = 'http://localhost:8000/shopping-bag/';

export const useAddToShoppingBag = () => {
    const { post } = useApi();
    const { isAuthenticated } = useAuth();
    const { setGuestDataHandler } = useGuest();

    const addToBag = useCallback(
        async ({ contentType, objectId, quantity }) => {
            const data = {
                content_type: contentType,
                object_id: objectId,
                quantity: quantity
            };

            if (!isAuthenticated) {
                setGuestDataHandler();
            }

            try {
                const response = await post(baseUrl, {
                    data
                    // accessRequired: true,
                    // refreshRequired: true
                });

                return response;
            } catch (err) {
                console.error('Error in addToBag:', err.message);
                throw err;
            }
        },
        [post, isAuthenticated, setGuestDataHandler]
    );

    return { addToBag };
};

export const useGetShoppingBagItems = () => {
    const { get } = useApi();

    const getShoppingBagItems = useCallback(async () => {
        try {
            const response = await get(baseUrl, {
                accessRequired: true,
                refreshRequired: true
            });

            return response;
        } catch (err) {
            console.log(err.message);
        }
    }, [get]);

    return {
        getShoppingBagItems
    };
};
