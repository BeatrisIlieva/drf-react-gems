import { useCallback } from 'react';

import { useApi } from '../hooks/useApi';

import { keysToCamelCase } from '../utils/convertToCamelCase';

import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/wishlist`;

export const useWishlist = () => {
    const { get, post, del } = useApi();

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

    const createItem = useCallback(
        async data => {
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
        async params => {
            try {
                await del(`${baseUrl}/remove/${params.content_type}/${params.object_id}/`, {
                    accessRequired: true,
                    refreshRequired: true,
                });

                return true;
            } catch (error) {
                console.error(error);
            }
        },
        [del]
    );

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

    return {
        getItems,
        createItem,
        deleteItem,
        getCount,
    };
};
