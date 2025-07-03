import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';
import { useShoppingBagContext } from '../contexts/ShoppingBagContext';
import { keysToCamelCase } from '../utils/convertToCamelCase';
import { useAuth } from '../hooks/auth/useAuth';
import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/shopping-bags`;

export const useShoppingBag = () => {
    const { get, post, put, del } = useApi();
    const { isAuthenticated } = useAuth();
    const {
        updateShoppingBagCount,
        updateShoppingBagTotalPrice
    } = useShoppingBagContext();

    // Create shopping bag item
    const createItem = useCallback(
        async ({ contentType, objectId, quantity }) => {
            const data = {
                content_type: contentType,
                object_id: objectId,
                quantity: quantity
            };
            try {
                const response = await post(`${baseUrl}/`, {
                    data,
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated
                });
                updateShoppingBagCount();

                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
            }
        },
        [post, isAuthenticated, updateShoppingBagCount]
    );

    // Delete shopping bag item
    const deleteItem = useCallback(
        async (bagItemId) => {
            try {
                const response = del(`${baseUrl}/${bagItemId}/`, {
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated
                });

                updateShoppingBagCount();
                updateShoppingBagTotalPrice();

                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
            }
        },
        [
            del,
            isAuthenticated,
            updateShoppingBagCount,
            updateShoppingBagTotalPrice
        ]
    );

    // Update shopping bag item
    const updateItem = useCallback(
        async ({ contentType, objectId, quantity, id }) => {
            if (quantity <= 0) {
                await deleteItem(id);
                return { success: true };
            }

            const data = {
                content_type: contentType,
                object_id: objectId,
                quantity: quantity
            };

            try {
                const response = await put(`${baseUrl}/${id}/`, {
                    data,
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated
                });

                updateShoppingBagCount();
                updateShoppingBagTotalPrice();

                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
            }
        },
        [
            put,
            isAuthenticated,
            updateShoppingBagCount,
            updateShoppingBagTotalPrice,
            deleteItem
        ]
    );

    // Get all shopping bag items
    const getItems = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error(error);
        }
    }, [get, isAuthenticated]);

    // Get shopping bag count
    const getCount = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/count/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error(error);
        }
    }, [get, isAuthenticated]);

    // Get shopping bag total price
    const getTotalPrice = useCallback(async () => {
        try {
            const response = await get(
                `${baseUrl}/total-price/`,
                {
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated
                }
            );

            return keysToCamelCase(response);
        } catch (error) {
            console.error(error);
        }
    }, [get, isAuthenticated]);

    return {
        createItem,
        updateItem,
        deleteItem,
        getItems,
        getCount,
        getTotalPrice
    };
};
