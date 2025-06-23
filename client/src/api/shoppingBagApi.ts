import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';
import { useAuth } from '../hooks/auth/useAuth';
import { useShoppingBagContext } from '../contexts/ShoppingBagContext';
import type { AddToBagParams } from '../types/ShoppingBag';
import { keysToCamelCase } from '../utils/convertToCamelCase';

const baseUrl = 'http://localhost:8000/shopping-bags/';

interface ApiResponse<T = any> {
    data?: T;
    status?: number;
    error?: string;
}

export const useAddToShoppingBag = () => {
    const { post } = useApi();
    const { isAuthenticated } = useAuth();
    const { updateShoppingBagCount } = useShoppingBagContext();

    const addToBag = useCallback(
        async ({
            contentType,
            objectId,
            quantity
        }: AddToBagParams): Promise<ApiResponse> => {
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

    const getShoppingBagItems = useCallback(async (): Promise<
        ApiResponse | undefined
    > => {
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

    const getShoppingBagCount = useCallback(async (): Promise<
        ApiResponse | undefined
    > => {
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
        useCallback(async (): Promise<
            ApiResponse | undefined
        > => {
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
