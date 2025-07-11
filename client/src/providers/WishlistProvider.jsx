import { useCallback, useContext, useEffect, useMemo, useState } from 'react';

import { useWishlist } from '../api/wishlistApi';

import { useGuest } from '../hooks/useGuest';
import usePersistedState from '../hooks/usePersistedState';

import { UserContext } from '../contexts/UserContext';
import { WishlistContext } from '../contexts/WishlistContext';

export const WishlistProvider = ({ children }) => {
    const [loading, setLoading] = useState(true);
    const { guestData } = useGuest();
    const [wishlistItemsCount, setWishlistItemsCount] = usePersistedState('wishlist-count', 0);
    const [wishlistItems, setWishlistItems] = usePersistedState('wishlist-items', []);

    const { getItems, createItem, deleteItem } = useWishlist();
    const { id: userId } = useContext(UserContext);

    const addToWishlist = useCallback(
        async (contentType, objectId) => {
            try {
                const requestData = {
                    content_type: contentType,
                    object_id: objectId,
                };

                const newItem = await createItem(requestData);
                if (newItem) {
                    const transformedItem = {
                        ...newItem.productInfo,
                        contentType: newItem.contentType,
                        objectId: newItem.objectId,
                        wishlistId: newItem.id,
                        categoryName: `${newItem.contentType}s`,
                    };
                    setWishlistItems(prev => [...prev, transformedItem]);
                    setWishlistItemsCount(prev => prev + 1);
                    return true;
                }
                return false;
            } catch {
                return false;
            }
        },
        [createItem]
    );

    const removeFromWishlist = useCallback(
        async (contentType, objectId) => {
            try {
                const success = await deleteItem({
                    content_type: contentType,
                    object_id: objectId,
                });

                if (success) {
                    setWishlistItems(prev =>
                        prev.filter(
                            item =>
                                !(item.contentType === contentType && item.objectId === objectId)
                        )
                    );
                    setWishlistItemsCount(prev => Math.max(0, prev - 1));
                    return true;
                }
                return false;
            } catch {
                return false;
            }
        },
        [deleteItem]
    );

    const isInWishlist = useCallback(
        (contentType, objectId) => {
            if (!contentType || !objectId) return false;

            const standardizedContentType = contentType.endsWith('s')
                ? contentType.slice(0, -1)
                : contentType;

            return wishlistItems.some(item => {
                const itemContentType = item.contentType?.endsWith('s')
                    ? item.contentType.slice(0, -1)
                    : item.contentType;

                const objectIdStr = String(objectId);

                const idMatches =
                    String(item.objectId) === objectIdStr ||
                    String(item.productId) === objectIdStr ||
                    String(item.id) === objectIdStr;

                let categoryMatches = false;
                if (item.category) {
                    const itemCategory =
                        typeof item.category === 'string'
                            ? item.category.toLowerCase()
                            : item.category.name?.toLowerCase();

                    categoryMatches = itemCategory === standardizedContentType;
                }

                const contentTypeMatches =
                    itemContentType === standardizedContentType || categoryMatches;

                return contentTypeMatches && idMatches;
            });
        },
        [wishlistItems]
    );

    const handleWishlistToggle = useCallback(
        async (categoryName, id) => {
            const category = categoryName?.slice(0, categoryName?.length - 1);

            if (category && id) {
                if (isInWishlist(category, id)) {
                    await removeFromWishlist(category, id);
                } else {
                    await addToWishlist(category, id);
                }
            }
        },
        [addToWishlist, removeFromWishlist, isInWishlist]
    );

    useEffect(() => {
        let mounted = true;

        const loadWishlist = async () => {
            if (!userId && !guestData.guest_id) {
                setWishlistItems([]);
                setWishlistItemsCount(0);
                setLoading(false);
                return;
            }

            setLoading(true);
            try {
                const response = await getItems();
                if (response && Array.isArray(response) && mounted) {
                    const transformedItems = response.map(item => ({
                        ...item.productInfo,
                        contentType: item.contentType,
                        objectId: item.objectId,
                        wishlistId: item.id,
                        categoryName: `${item.contentType}s`,
                    }));
                    setWishlistItems(transformedItems);
                    setWishlistItemsCount(transformedItems.length);
                } else if (mounted) {
                    setWishlistItems([]);
                    setWishlistItemsCount(0);
                }
            } catch {
                if (mounted) {
                    setWishlistItems([]);
                    setWishlistItemsCount(0);
                }
            } finally {
                if (mounted) {
                    setLoading(false);
                }
            }
        };

        loadWishlist();

        return () => {
            mounted = false;
        };
    }, [userId, getItems]);

    const refreshWishlist = useCallback(async () => {
        try {
            const response = await getItems();
            if (response && Array.isArray(response)) {
                const transformedItems = response.map(item => ({
                    ...item.productInfo,
                    contentType: item.contentType,
                    objectId: item.objectId,
                    wishlistId: item.id,
                    categoryName: `${item.contentType}s`,
                }));
                setWishlistItems(transformedItems);
                setWishlistItemsCount(transformedItems.length);
            } else {
                setWishlistItems([]);
                setWishlistItemsCount(0);
            }
        } catch {
            setWishlistItems([]);
            setWishlistItemsCount(0);
        }
    }, [getItems]);

    const contextValue = useMemo(
        () => ({
            wishlistItems,
            wishlistItemsCount,
            loading,
            addToWishlist,
            removeFromWishlist,
            isInWishlist,
            handleWishlistToggle,
            refreshWishlist,
        }),
        [
            wishlistItems,
            wishlistItemsCount,
            loading,
            addToWishlist,
            removeFromWishlist,
            isInWishlist,
            handleWishlistToggle,
            refreshWishlist,
        ]
    );

    return <WishlistContext.Provider value={contextValue}>{children}</WishlistContext.Provider>;
};
