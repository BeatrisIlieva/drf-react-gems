import { useMemo,  useState, useEffect, useCallback, useContext } from "react";
import { WishlistContext} from "../contexts/WishlistContext";
import { useWishlistApi } from "../api/wishlistApi";
import { UserContext } from "../contexts/UserContext";


export const WishlistProvider = ({ children }) => {
    const [wishlistItems, setWishlistItems] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    
    const { getWishlist, addToWishlist: apiAddToWishlist, removeFromWishlist: apiRemoveFromWishlist } = useWishlistApi();
    const { id: userId } = useContext(UserContext);

    const refreshWishlist = useCallback(async () => {
        setIsLoading(true);
        try {
            const response = await getWishlist();
            if (response && Array.isArray(response)) {
                setWishlistItems(response);
            }
        } catch (error) {
            console.error('Failed to refresh wishlist:', error);
        } finally {
            setIsLoading(false);
        }
        // Only include userId as dependency to avoid recreating this function unnecessarily
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [userId]);

    const addToWishlist = useCallback(async (contentType, objectId) => {
        try {
            const requestData = {
                content_type: contentType,
                object_id: objectId
            };

            const newItem = await apiAddToWishlist(requestData);
            if (newItem) {
                setWishlistItems(prev => [...prev, newItem]);
                return true;
            }
            return false;
        } catch (error) {
            console.error('Failed to add to wishlist:', error);
            return false;
        }
        // Only include userId as dependency to avoid recreating this function unnecessarily
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [userId]);

    const removeFromWishlist = useCallback(async (contentType, objectId) => {
        try {
            const success = await apiRemoveFromWishlist({
                content_type: contentType,
                object_id: objectId
            });

            if (success) {
                setWishlistItems(prev => 
                    prev.filter(item => 
                        !(item.content_type === contentType && item.object_id === objectId)
                    )
                );
                return true;
            }
            return false;
        } catch (error) {
            console.error('Failed to remove from wishlist:', error);
            return false;
        }
        // Only include userId as dependency to avoid recreating this function unnecessarily
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [userId]);

    const isInWishlist = useCallback((contentType, objectId) => {
        return wishlistItems.some(item => 
            item.content_type === contentType && item.object_id === objectId
        );
    }, [wishlistItems]);

    const wishlistCount = useMemo(() => wishlistItems.length, [wishlistItems]);

    const updateWishlistCount = useCallback(async () => {
        // Since count is derived from wishlistItems.length, 
        // we just need to refresh the items
        await refreshWishlist();
    }, [refreshWishlist]);

    // Load wishlist on mount and when authentication state changes
    useEffect(() => {
        const loadWishlist = async () => {
            setIsLoading(true);
            try {
                const response = await getWishlist();
                if (response && Array.isArray(response)) {
                    setWishlistItems(response);
                }
            } catch (error) {
                console.error('Failed to refresh wishlist:', error);
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
            wishlistCount,
            isLoading,
            addToWishlist,
            removeFromWishlist,
            isInWishlist,
            refreshWishlist,
            updateWishlistCount
        }), 
        [wishlistItems, wishlistCount, isLoading, addToWishlist, removeFromWishlist, isInWishlist, refreshWishlist, updateWishlistCount]
    );

    return (
        <WishlistContext.Provider value={contextValue}>
            {children}
        </WishlistContext.Provider>
    );
};


