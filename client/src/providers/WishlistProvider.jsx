import { useCallback, useContext, useEffect, useMemo, useState } from 'react';

import { useWishlist } from '../api/wishlistApi';

import usePersistedState from '../hooks/usePersistedState';

import { UserContext } from '../contexts/UserContext';
import { WishlistContext } from '../contexts/WishlistContext';

export const WishlistProvider = ({ children }) => {
    const [loading, setLoading] = useState(true);
    const [wishlistItemsCount, setWishlistItemsCount] = usePersistedState('wishlist-count', 0);
    const [wishlistItems, setWishlistItems] = usePersistedState('wishlist-items', []);
    const migratedItemsData = JSON.parse(localStorage.getItem('migratedWishlist'));
    const migratedItems = migratedItemsData;

    const { getItems, createItem, deleteItem } = useWishlist();
    const { id: userId } = useContext(UserContext);

    const loadWishlist = useCallback(async () => {
        setLoading(true);
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
            }
        } catch {
            setWishlistItems([]);
            setWishlistItemsCount(0);
        } finally {
            setLoading(false);
        }
    }, [getItems, setWishlistItems, setWishlistItemsCount]);

    const migrateItemsToWishlist = useCallback(async () => {
        for (const item of wishlistItems) {
            const requestData = {
                content_type: item.contentType,
                object_id: item.objectId,
            };
            await createItem(requestData);
        }
    }, [createItem, wishlistItems]);

    useEffect(() => {
        if (userId && !migratedItems) {
            migrateItemsToWishlist().then(() => {
                localStorage.setItem('migratedWishlist', true);
                loadWishlist();
            });
        }
    }, [loadWishlist, migrateItemsToWishlist, userId, migratedItems]);

    useEffect(() => {
        if (!userId) {
            const wishlistItems = localStorage.getItem('wishlist-items');
            setWishlistItems(wishlistItems ? JSON.parse(wishlistItems) : []);

            const wishlistCount = localStorage.getItem('shopping-bag-count');
            setWishlistItemsCount(wishlistCount ? parseInt(wishlistCount, 10) : 0);
            setLoading(false);
            return;
        }

        loadWishlist();
    }, [userId, setWishlistItems, setWishlistItemsCount, loadWishlist]);

    const addToWishlist = useCallback(
        async (
            contentType,
            objectId,
            collectionName = null,
            firstImage = null,
            secondImage = null,
            colorName = null,
            stoneName = null,
            metalName = null,
            minPrice = null,
            maxPrice = null,
            averageRating = null
        ) => {
            if (!userId) {
                const data = {
                    categoryName: `${contentType}s`,
                    contentType,
                    objectId,
                    id: objectId,
                    collectionName,
                    firstImage,
                    secondImage,
                    colorName,
                    stoneName,
                    metalName,
                    minPrice,
                    maxPrice,
                    averageRating,
                };
                setWishlistItems(prev => [data, ...prev]);
                setWishlistItemsCount(prev => prev + 1);

                return true;
            }
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
                let success = true;
                if (userId) {
                    success = await deleteItem({
                        content_type: contentType,
                        object_id: objectId,
                    });
                }

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
        async (
            categoryName,
            id,
            collectionName = null,
            firstImage = null,
            secondImage = null,
            colorName = null,
            stoneName = null,
            metalName = null,
            minPrice = null,
            maxPrice = null,
            averageRating = null
        ) => {
            const category = categoryName?.slice(0, categoryName?.length - 1);

            if (category && id) {
                if (isInWishlist(category, id)) {
                    await removeFromWishlist(category, id);
                } else {
                    await addToWishlist(
                        category,
                        id,
                        collectionName,
                        firstImage,
                        secondImage,
                        colorName,
                        stoneName,
                        metalName,
                        minPrice,
                        maxPrice,
                        averageRating
                    );
                }
            }
        },
        [addToWishlist, removeFromWishlist, isInWishlist]
    );

    useEffect(() => {
        setWishlistItemsCount(Array.isArray(wishlistItems) ? wishlistItems.length : 0);
    }, [wishlistItems, setWishlistItemsCount]);

    const refreshWishlist = useCallback(async () => {
        if (!userId) {
            return;
        }
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
