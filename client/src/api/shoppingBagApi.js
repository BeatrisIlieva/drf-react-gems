import { useCallback } from 'react';

import { useApi } from '../hooks/useApi';

import { keysToCamelCase } from '../utils/convertToCamelCase';

import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/shopping-bags`;

export const useShoppingBag = () => {
    const { get, post, put, del } = useApi();

    const createItem = useCallback(
        async ({ inventory, quantity }) => {
            const data = {
                inventory,
                quantity,
            };
            try {
                const response = await post(`${baseUrl}/`, {
                    data,
                    accessRequired: true,
                    refreshRequired: true,
                });

                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
            }
        },
        [post]
    );

    const deleteItem = useCallback(
        async bagItemId => {
            try {
                const response = del(`${baseUrl}/${bagItemId}/`, {
                    accessRequired: true,
                    refreshRequired: true,
                });

                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
            }
        },
        [del]
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
                    accessRequired: true,
                    refreshRequired: true,
                });

                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
            }
        },
        [put, deleteItem]
    );

    const getItems = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/`, {
                accessRequired: true,
                refreshRequired: true,
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error(error);
        }
    }, [get]);

    const getCount = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/count/`, {
                accessRequired: true,
                refreshRequired: true,
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error(error);
        }
    }, [get]);

    const getTotalPrice = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/total-price/`, {
                accessRequired: true,
                refreshRequired: true,
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error(error);
        }
    }, [get]);

    return {
        createItem,
        updateItem,
        deleteItem,
        getItems,
        getCount,
        getTotalPrice,
    };
};
