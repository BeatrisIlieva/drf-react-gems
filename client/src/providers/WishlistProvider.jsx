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

    const updateWishlistCount = useCallback(async () => {
        try {
            const response = await getCount();
            if (response) {
                setWishlistItemsCount(response.count);
            }
        } catch (err) {
            console.error(err.message);
        }
    }, [getCount]);

    const addToWishlist = useCallback(
        async (contentType, objectId) => {
            try {
                const requestData = {
                    content_type: contentType,
                    object_id: objectId
                };

                const newItem = await createItem(requestData);
                if (newItem) {
                    const transformedItem = {
                        ...newItem.productInfo,
                        contentType: newItem.contentType,
                        objectId: newItem.objectId,
                        wishlistId: newItem.id,
                        categoryName: `${newItem.contentType}s`
                    };
                    setWishlistItems((prev) => [
                        ...prev,
                        transformedItem
                    ]);
                    setWishlistItemsCount((prev) => prev + 1);
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
        [createItem]
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
                                    item.contentType ===
                                        contentType &&
                                    item.objectId === objectId
                                )
                        )
                    );
                    setWishlistItemsCount((prev) =>
                        Math.max(0, prev - 1)
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
        [deleteItem]
    );

    const isInWishlist = useCallback(
        (contentType, objectId) => {
            if (!contentType || !objectId) return false;
            
            // Standardize contentType format for comparison (handle singular/plural)
            const standardizedContentType = contentType.endsWith('s') 
                ? contentType.slice(0, -1) 
                : contentType;
            
            return wishlistItems.some(
                (item) => {
                    // Standardize item's contentType
                    const itemContentType = item.contentType?.endsWith('s')
                        ? item.contentType.slice(0, -1)
                        : item.contentType;
                    
                    // Convert all ID values to strings for comparison
                    const objectIdStr = String(objectId);
                    
                    // Match using different possible ID fields
                    const idMatches = 
                        String(item.objectId) === objectIdStr || 
                        String(item.productId) === objectIdStr ||
                        String(item.id) === objectIdStr;
                    
                    // Check if category field exists and match it
                    let categoryMatches = false;
                    if (item.category) {
                        const itemCategory = typeof item.category === 'string' 
                            ? item.category.toLowerCase() 
                            : item.category.name?.toLowerCase();
                        
                        categoryMatches = itemCategory === standardizedContentType;
                    }
                    
                    // Match using different possible contentType fields
                    const contentTypeMatches =
                        itemContentType === standardizedContentType || categoryMatches;
                    
                    return contentTypeMatches && idMatches;
                }
            );
        },
        [wishlistItems]
    );

    const handleWishlistToggle = useCallback(
        async (categoryName, id) => {
            const category = categoryName?.slice(
                0,
                categoryName?.length - 1
            );

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
        const loadWishlist = async () => {
            setIsLoading(true);
            try {
                const response = await getItems();
                if (response && Array.isArray(response)) {
                    const transformedItems = response.map(
                        (item) => ({
                            ...item.productInfo,
                            contentType: item.contentType,
                            objectId: item.objectId,
                            wishlistId: item.id,
                            categoryName: `${item.contentType}s`
                        })
                    );
                    setWishlistItems(transformedItems);
                    setWishlistItemsCount(
                        transformedItems.length
                    );
                } else {
                    setWishlistItems([]);
                    setWishlistItemsCount(0);
                }
            } catch (error) {
                console.error(
                    'Failed to refresh wishlist:',
                    error
                );
                setWishlistItems([]);
                setWishlistItemsCount(0);
            } finally {
                setIsLoading(false);
            }
        };

        loadWishlist();
    }, [userId, getItems]);

    const contextValue = useMemo(
        () => ({
            wishlistItems,
            wishlistItemsCount,
            isLoading,
            addToWishlist,
            removeFromWishlist,
            isInWishlist,
            updateWishlistCount,
            handleWishlistToggle
        }),
        [
            wishlistItems,
            wishlistItemsCount,
            isLoading,
            addToWishlist,
            removeFromWishlist,
            isInWishlist,
            updateWishlistCount,
            handleWishlistToggle
        ]
    );

    return (
        <WishlistContext.Provider value={contextValue}>
            {children}
        </WishlistContext.Provider>
    );
};
