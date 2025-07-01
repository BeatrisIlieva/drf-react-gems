import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';
import { HOST } from '../constants/host';

import { useAuth } from '../hooks/auth/useAuth';

const baseUrl = `${HOST}/wishlist`;

export const useWishlistApi = () => {
    const { get, post, del } = useApi();
    const { isAuthenticated } = useAuth();

    const getWishlist = useCallback(async () => {
        try {
            const result = await get(`${baseUrl}/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });
            return result;
        } catch (error) {
            console.error('Error fetching wishlist:', error);
            return undefined;
        }
    }, [get, isAuthenticated]);

    const addToWishlist = useCallback(
        async (data) => {
            try {
                const result = await post(`${baseUrl}/add/`, {
                    data,
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated
                });
                return result;
            } catch (error) {
                console.error('Error adding to wishlist:', error);
                return undefined;
            }
        },
        [post, isAuthenticated]
    );

    const removeFromWishlist = useCallback(
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
                console.error(
                    'Error removing from wishlist:',
                    error
                );
                return false;
            }
        },
        [del, isAuthenticated]
    );

    const getWishlistCount = useCallback(async () => {
        try {
            const result = await get(`${baseUrl}/count/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });
            return result?.count || 0;
        } catch (error) {
            console.error(
                'Error fetching wishlist count:',
                error
            );
            return 0;
        }
    }, [get, isAuthenticated]);

    return {
        getWishlist,
        addToWishlist,
        removeFromWishlist,
        getWishlistCount
    };
};
