import {
    useMemo,
    useState,
    useEffect,
    useCallback,
    useContext
} from 'react';
import { WishlistContext } from '../contexts/WishlistContext';
import { UserContext } from '../contexts/UserContext';
import { useWishlist } from '../api/wishlistApi';

export const WishlistProvider = ({ children }) => {
    const [wishlistItems, setWishlistItems] = useState([]);
    const [wishlistItemsCount, setWishlistItemsCount] =
        useState(0);
    const [isLoading, setIsLoading] = useState(false);

    const { getItems, createItem, deleteItem, getCount } =
        useWishlist();
    const { id: userId } = useContext(UserContext);

    const addToWishlist = useCallback(
        async (contentType, objectId) => {
            try {
                const requestData = {
                    content_type: contentType,
                    object_id: objectId
                };

                const newItem = await createItem(requestData);
                if (newItem) {
                    setWishlistItems((prev) => [
                        ...prev,
                        newItem
                    ]);
                    return true;
                }
                return false;
            } catch (error) {
                console.error(
                    'Failed to add to wishlist:',
                    error
                );
                return false;
            }
        },
        [userId]
    );

    const removeFromWishlist = useCallback(
        async (contentType, objectId) => {
            try {
                const success = await deleteItem({
                    content_type: contentType,
                    object_id: objectId
                });

                if (success) {
                    setWishlistItems((prev) =>
                        prev.filter(
                            (item) =>
                                !(
                                    item.content_type ===
                                        contentType &&
                                    item.object_id === objectId
                                )
                        )
                    );
                    return true;
                }
                return false;
            } catch (error) {
                console.error(
                    'Failed to remove from wishlist:',
                    error
                );
                return false;
            }
        },
        [userId]
    );

    const isInWishlist = useCallback(
        (contentType, objectId) => {
            return wishlistItems.some(
                (item) =>
                    item.content_type === contentType &&
                    item.object_id === objectId
            );
        },
        [wishlistItems]
    );

    const updateWishlistCount = useCallback(async () => {
        try {
            const response = await getCount();
            if (response) {
                setWishlistItemsCount(response.count);
            }
        } catch (err) {
            console.error(
                'Error updating shopping bag count:',
                err instanceof Error ? err.message : String(err)
            );
        }
    }, [getCount]);

    // Load wishlist on mount and when authentication state changes
    useEffect(() => {
        const loadWishlist = async () => {
            setIsLoading(true);
            try {
                const response = await getItems();
                if (response && Array.isArray(response)) {
                    setWishlistItems(response);
                }
            } catch (error) {
                console.error(
                    'Failed to refresh wishlist:',
                    error
                );
            } finally {
                setIsLoading(false);
            }
        };

        loadWishlist();
        // Only depend on userId (stable) instead of the entire getWishlist function
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [userId]);

    const contextValue = useMemo(
        () => ({
            wishlistItems,
            wishlistItemsCount,
            isLoading,
            addToWishlist,
            removeFromWishlist,
            isInWishlist,
            updateWishlistCount
        }),
        [
            wishlistItems,
            wishlistItemsCount,
            isLoading,
            addToWishlist,
            removeFromWishlist,
            isInWishlist,
            updateWishlistCount
        ]
    );

    return (
        <WishlistContext.Provider value={contextValue}>
            {children}
        </WishlistContext.Provider>
    );
};
