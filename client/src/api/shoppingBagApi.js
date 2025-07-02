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
            } catch (err) {
                console.error(
                    'Error in createItem:',
                    err.message
                );
                throw err;
            }
        },
        [post, isAuthenticated, updateShoppingBagCount]
    );

    // Delete shopping bag item
    const deleteItem = useCallback(
        async (bagItemId) => {
            try {
                await del(`${baseUrl}${bagItemId}/`, {
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated
                });

                // Update context after successful deletion
                updateShoppingBagCount();
                updateShoppingBagTotalPrice();

                return;
            } catch (err) {
                console.error(
                    'Error in deleteItem:',
                    err instanceof Error
                        ? err.message
                        : String(err)
                );
                throw err;
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
                const response = await put(`${baseUrl}${id}/`, {
                    data,
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated
                });

                // Update both count and total price when bag is updated
                updateShoppingBagCount();
                updateShoppingBagTotalPrice();

                return keysToCamelCase(response);
            } catch (err) {
                if (
                    err.response?.data?.detail?.includes(
                        'Not enough quantity in inventory'
                    )
                ) {
                    throw new Error(
                        "Sorry, we don't have enough items in stock."
                    );
                }

                console.error(
                    'Error in updateItem:',
                    err.message
                );
                throw err;
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
        } catch (err) {
            console.log(err.message);
            return undefined;
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
        } catch (err) {
            console.log(err.message);
            return undefined;
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
        } catch (err) {
            console.log(err.message);
            return undefined;
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
