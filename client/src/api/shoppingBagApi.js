import { useCallback } from 'react';

import { useApi } from '../hooks/useApi';
import { useAuth } from '../hooks/useAuth';

import { keysToCamelCase } from '../utils/convertToCamelCase';

import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/shopping-bags`;

export const useShoppingBag = () => {
    const { get, post, put, del } = useApi();
    const { isAuthenticated } = useAuth();

    const createItem = useCallback(
        async ({ inventory, quantity }) => {
            const data = {
                inventory,
                quantity,
            };
            try {
                const response = await post(`${baseUrl}/`, {
                    data,
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated,
                });

                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
            }
        },
        [post, isAuthenticated]
    );

    const deleteItem = useCallback(
        async bagItemId => {
            try {
                const response = del(`${baseUrl}/${bagItemId}/`, {
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated,
                });

                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
            }
        },
        [del, isAuthenticated]
    );

    const updateItem = useCallback(
        async ({ inventory, quantity, id }) => {
            if (quantity <= 0) {
                await deleteItem(id);
                return { success: true };
            }

            const data = {
                inventory,
                quantity,
            };

            try {
                const response = await put(`${baseUrl}/${id}/`, {
                    data,
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated,
                });

                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
            }
        },
        [put, isAuthenticated, deleteItem]
    );

    const getItems = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated,
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error(error);
        }
    }, [get, isAuthenticated]);

    const getCount = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/count/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated,
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error(error);
        }
    }, [get, isAuthenticated]);

    const getTotalPrice = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/total-price/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated,
            });

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
        getTotalPrice,
    };
};
