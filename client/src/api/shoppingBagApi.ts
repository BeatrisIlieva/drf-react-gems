import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';
import { useAuth } from '../hooks/auth/useAuth';
import { useShoppingBagContext } from '../contexts/ShoppingBagContext';
import type {
    CreateShoppingBagParams,
    ShoppingBagItemResponse
} from '../types/ShoppingBag';
import { keysToCamelCase } from '../utils/convertToCamelCase';

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

export const useDeleteShoppingBag = () => {
    const { del } = useApi();
    const { isAuthenticated } = useAuth();
    const { updateShoppingBagCount } = useShoppingBagContext();

    const deleteShoppingBag = useCallback(
        async (bagItemId: number | string): Promise<void> => {
            try {
                await del(`${baseUrl}${bagItemId}/`, {
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated
                });

                updateShoppingBagCount();
            } catch (err: any) {
                console.error(
                    'Error in deleteShoppingBag:',
                    err.message
                );
                throw err;
            }
        },
        [del, isAuthenticated, updateShoppingBagCount]
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
