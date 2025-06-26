import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';

import { useShoppingBagContext } from '../contexts/ShoppingBagContext';
import type {
    CreateShoppingBagParams,
    ShoppingBagItemResponse,
    UpdateShoppingBagParams
} from '../types/ShoppingBag';
import { keysToCamelCase } from '../utils/convertToCamelCase';
import { useAuth } from '../hooks/auth/useAuth';

const baseUrl = 'http://localhost:8000/shopping-bags/';

export const useCreateShoppingBag = () => {
    const { post } = useApi();
    const { isAuthenticated } = useAuth();
    const { updateShoppingBagCount } = useShoppingBagContext();

    const createShoppingBag = useCallback(
        async ({
            contentType,
            objectId,
            quantity
        }: CreateShoppingBagParams): Promise<ShoppingBagItemResponse> => {
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

                return keysToCamelCase(response);
            } catch (err: any) {
                console.error(
                    'Error in createShoppingBag:',
                    err.message
                );
                throw err;
            }
        },
        [post, isAuthenticated, updateShoppingBagCount]
    );

    return { createShoppingBag };
};

export const useUpdateShoppingBag = () => {
    const { put } = useApi();
    const { isAuthenticated } = useAuth();
    const {
        updateShoppingBagCount,
        updateShoppingBagTotalPrice
    } = useShoppingBagContext();
    const { deleteShoppingBag } = useDeleteShoppingBag();

    const updateShoppingBag = useCallback(
        async ({
            contentType,
            objectId,
            quantity,
            id
        }: UpdateShoppingBagParams): Promise<ShoppingBagItemResponse> => {
            if (quantity <= 0) {
                await deleteShoppingBag(id);
                return { success: true } as any;
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
            } catch (err: any) {
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
                    'Error in updateShoppingBag:',
                    err.message
                );
                throw err;
            }
        },
        [
            put,
            isAuthenticated,
            updateShoppingBagCount,
            deleteShoppingBag,
            updateShoppingBagTotalPrice
        ]
    );

    return { updateShoppingBag };
};

export const useDeleteShoppingBag = () => {
    const { del } = useApi();
    const { isAuthenticated } = useAuth();

    const deleteShoppingBag = useCallback(
        async (bagItemId: number | string): Promise<void> => {
            try {
                // DELETE requests typically return null/undefined for successful deletions
                await del(`${baseUrl}${bagItemId}/`, {
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated
                });

                // For delete operations, we don't need to return anything
                // The success is indicated by not throwing an error
                return;
            } catch (err: any) {
                console.error(
                    'Error in deleteShoppingBag:',
                    err instanceof Error
                        ? err.message
                        : String(err)
                );
                throw err;
            }
        },
        [del, isAuthenticated]
    );

    return { deleteShoppingBag };
};

export const useGetShoppingBagItems = () => {
    const { get } = useApi();
    const { isAuthenticated } = useAuth();

    const getShoppingBagItems =
        useCallback(async (): Promise<any> => {
            try {
                const response = await get(baseUrl, {
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated
                });

                return keysToCamelCase(response);
            } catch (err: any) {
                console.log(err.message);
                return undefined;
            }
        }, [get, isAuthenticated]);

    return {
        getShoppingBagItems
    };
};

export const useGetShoppingBagCount = () => {
    const { get } = useApi();
    const { isAuthenticated } = useAuth();

    const getShoppingBagCount =
        useCallback(async (): Promise<any> => {
            try {
                const response = await get(`${baseUrl}count/`, {
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated
                });

                return keysToCamelCase(response);
            } catch (err: any) {
                console.log(err.message);
                return undefined;
            }
        }, [get, isAuthenticated]);

    return {
        getShoppingBagCount
    };
};

export const useGetShoppingBagTotalPrice = () => {
    const { get } = useApi();
    const { isAuthenticated } = useAuth();

    const getShoppingBagTotalPrice =
        useCallback(async (): Promise<any> => {
            try {
                const response = await get(
                    `${baseUrl}total-price/`,
                    {
                        accessRequired: isAuthenticated,
                        refreshRequired: isAuthenticated
                    }
                );

                return keysToCamelCase(response);
            } catch (err: any) {
                console.log(err.message);
                return undefined;
            }
        }, [get, isAuthenticated]);

    return {
        getShoppingBagTotalPrice
    };
};
