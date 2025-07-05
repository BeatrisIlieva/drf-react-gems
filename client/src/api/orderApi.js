import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';
import { keysToCamelCase } from '../utils/convertToCamelCase';
import { keysToSnakeCase } from '../utils/convertToSnakeCase';
import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/orders`;

export const useOrder = () => {
    const { get, post } = useApi();

    // Create order from shopping bag with payment data
    const createOrderFromBag = useCallback(
        async (paymentData) => {
            const data = keysToSnakeCase(paymentData);

            try {
                const response = await post(
                    `${baseUrl}/create-from-bag/`,
                    {
                        data,
                        accessRequired: true,
                        refreshRequired: true
                    }
                );

                return keysToCamelCase(response);
            } catch (error) {
                console.error('Order creation error:', error);
                throw error;
            }
        },
        [post]
    );

    // Get all orders for the user
    const getOrders = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/`, {
                accessRequired: true,
                refreshRequired: true
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error('Get orders error:', error);
            throw error;
        }
    }, [get]);

    // Get order summary
    const getOrderSummary = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/summary/`, {
                accessRequired: true,
                refreshRequired: true
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error('Get order summary error:', error);
            throw error;
        }
    }, [get]);

    return {
        createOrderFromBag,
        getOrders,
        getOrderSummary
    };
};
