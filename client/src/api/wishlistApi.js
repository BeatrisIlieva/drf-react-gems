import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';
import { keysToCamelCase } from '../utils/convertToCamelCase';
import { HOST } from '../constants/host';

import { useAuth } from '../hooks/auth/useAuth';

const baseUrl = `${HOST}/api/wishlist`;

export const useWishlist = () => {
    const { get, post, del } = useApi();
    const { isAuthenticated } = useAuth();

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

    const createItem = useCallback(
        async (data) => {
            try {
                const response = await post(`${baseUrl}/`, {
                    data,
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated
                });
                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
            }
        },
        [post, isAuthenticated]
    );

    const deleteItem = useCallback(
        async (params) => {
            try {
                await del(
                    `${baseUrl}/remove/${params.content_type}/${params.object_id}/`,
                    {
                        accessRequired: isAuthenticated,
                        refreshRequired: isAuthenticated
                    }
                );

                return true;
            } catch (error) {
                console.error(error);
            }
        },
        [del, isAuthenticated]
    );

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

    return {
        getItems,
        createItem,
        deleteItem,
        getCount
    };
};
