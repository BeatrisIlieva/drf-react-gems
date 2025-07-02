import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';
import { HOST } from '../constants/host';

import { useAuth } from '../hooks/auth/useAuth';
import { useWishlistContext } from '../contexts/WishlistContext';

const baseUrl = `${HOST}/api/wishlist`;

export const useWishlist = () => {
    const { get, post, del } = useApi();
    const { isAuthenticated } = useAuth();
    const {updateWishlistCount} = useWishlistContext();

    const getItems = useCallback(async () => {
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

    const createItem = useCallback(
        async (data) => {
            try {
                const result = await post(`${baseUrl}/`, {
                    data,
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated
                });
                updateWishlistCount();
                return result;
            } catch (error) {
                console.error('Error adding to wishlist:', error);
                return undefined;
            }
        },
        [post, isAuthenticated, updateWishlistCount]
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
                updateWishlistCount();
                return true;
            } catch (error) {
                console.error(
                    'Error removing from wishlist:',
                    error
                );
                return false;
            }
        },
        [del, isAuthenticated, updateWishlistCount]
    );

    const getCount = useCallback(async () => {
        try {
            const result = await get(`${baseUrl}/count/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });
            return result;
        } catch (error) {
            console.error(
                'Error fetching wishlist count:',
                error
            );
            return { count: 0 };
        }
    }, [get, isAuthenticated]);

    return {
        getItems,
        createItem,
        deleteItem,
        getCount
    };
};
