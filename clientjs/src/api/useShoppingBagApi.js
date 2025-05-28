import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';
import { useAuth } from '../hooks/useAuth';
import { useShoppingBagContext } from '../contexts/ShoppingBagContext';

const baseUrl = 'http://localhost:8000/shopping-bag/';

export const useAddToShoppingBag = () => {
    const { post } = useApi();
    const { isAuthenticated } = useAuth();
    const { updateShoppingBagCount } = useShoppingBagContext();

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
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated
                });
                updateShoppingBagCount();
                return response;
            } catch (err) {
                console.error('Error in addToBag:', err.message);
                throw err;
            }
        },
        [post, isAuthenticated, updateShoppingBagCount]
    );

    return { addToBag };
};

export const useGetShoppingBagItems = () => {
    const { get } = useApi();
    const { isAuthenticated } = useAuth();

    const getShoppingBagItems = useCallback(async () => {
        try {
            const response = await get(baseUrl, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });

            return response;
        } catch (err) {
            console.log(err.message);
        }
    }, [get, isAuthenticated]);

    return {
        getShoppingBagItems
    };
};

export const useGetShoppingBagCount = () => {
    const { get } = useApi();
    const { isAuthenticated } = useAuth();

    const getShoppingBagCount = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}count/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });

            return response;
        } catch (err) {
            console.log(err.message);
        }
    }, [get, isAuthenticated]);

    return {
        getShoppingBagCount
    };
};
