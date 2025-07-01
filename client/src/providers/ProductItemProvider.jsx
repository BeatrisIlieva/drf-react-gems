import { useParams } from 'react-router';
import { useProductItem } from '../api/productItemApi';
import {
    useCallback,
    useEffect,
    useMemo,
    useState,
    useContext
} from 'react';
import { ProductItemContext } from '../contexts/ProductItemContext';
import { useShoppingBag } from '../api/shoppingBagApi';
import { WishlistContext } from '../contexts/WishlistContext';

export const ProductItemProvider = ({ children }) => {
    const { getProductItem } = useProductItem();
    const { categoryName, productId } = useParams();
    const { createItem } = useShoppingBag();
    const { addToWishlist, removeFromWishlist, isInWishlist } =
        useContext(WishlistContext);

    const [loading, setLoading] = useState(true);
    const [product, setProduct] = useState(null);
    const [selectedSize, setSelectedSize] = useState(null);
    const [notSelectedSizeError, setNotSelectedSizeError] =
        useState(null);
    const [selectedInventory, setSelectedInventory] =
        useState(null);
    const [addToCartError, setAddToCartError] = useState(null);

    const getProductItemHandler = useCallback(async () => {
        setLoading(true);
        try {
            const response = await getProductItem({
                categoryName,
                productId
            });
            setProduct(response.product);
        } catch (error) {
            console.error('Error fetching product item:', error);
        } finally {
            setLoading(false);
        }
    }, [categoryName, productId, getProductItem]);

    useEffect(() => {
        getProductItemHandler();
    }, [categoryName, productId, getProductItemHandler]);

    const createShoppingBagHandler = useCallback(async () => {
        if (selectedSize === null) {
            setNotSelectedSizeError(true);
            return;
        }

        setAddToCartError(null);
        try {
            await createItem(selectedInventory);

            // Update local inventory data instead of refetching everything
            if (product && selectedInventory) {
                setProduct((prevProduct) => {
                    if (!prevProduct) return null;

                    // Create a deep copy of the product to avoid mutating state directly
                    const updatedProduct = {
                        ...prevProduct,
                        inventory: prevProduct.inventory.map(
                            (item) => {
                                // If this is the added item, decrement its quantity
                                if (
                                    item.id ===
                                    selectedInventory.objectId
                                ) {
                                    return {
                                        ...item,
                                        // Ensure we never remove the item, just set quantity to 0
                                        quantity: Math.max(
                                            0,
                                            item.quantity -
                                                selectedInventory.quantity
                                        )
                                    };
                                }
                                return item;
                            }
                        )
                    };

                    return updatedProduct;
                });
            }

            // Reset selected size after successful add to bag
            setSelectedSize(null);
            setSelectedInventory(null);
        } catch (error) {
            console.error(
                'Error adding item to shopping bag:',
                error
            );

            // Detect inventory-related errors
            const errorMessage =
                error instanceof Error
                    ? error.message
                    : String(error);
            const isInventoryError =
                errorMessage.includes('inventory') ||
                errorMessage.includes('sold out') ||
                errorMessage.includes('stock') ||
                errorMessage.includes('quantity');

            if (isInventoryError) {
                // If this was an inventory error, refresh the product data
                await getProductItemHandler();
                setAddToCartError(
                    'This item is no longer available. The product information has been updated.'
                );
            } else {
                setAddToCartError(
                    "We couldn't add this item to your bag. Please try again later."
                );
            }

            setTimeout(() => {
                setAddToCartError(null);
            }, 1000);
        }
    }, [
        selectedSize,
        createItem,
        selectedInventory,
        product,
        getProductItemHandler
    ]);

    const addToWishlistHandler = useCallback(async () => {
        if (!product || !categoryName) return;

        const contentType = categoryName.slice(0, -1); // Remove 's' to make it singular
        const objectId = product.id;

        const isCurrentlyInWishlist = isInWishlist(
            contentType,
            objectId
        );

        if (isCurrentlyInWishlist) {
            await removeFromWishlist(contentType, objectId);
        } else {
            await addToWishlist(contentType, objectId);
        }
    }, [
        product,
        categoryName,
        isInWishlist,
        addToWishlist,
        removeFromWishlist
    ]);

    const updateSelectedInventoryHandler = (
        contentType,
        objectId
    ) => {
        setSelectedInventory({
            quantity: 1,
            contentType,
            objectId
        });
    };

    const setSelectedSizeHandler = useCallback(
        (size, contentType, objectId) => {
            if (selectedSize === null) {
                setSelectedSize(size);
                setNotSelectedSizeError(false);
                updateSelectedInventoryHandler(
                    contentType,
                    objectId
                );
            } else if (selectedSize === size) {
                setSelectedSize(null);
                setNotSelectedSizeError(null);
                setSelectedInventory(null);
            } else {
                setSelectedSize(size);
                setNotSelectedSizeError(false);
                updateSelectedInventoryHandler(
                    contentType,
                    objectId
                );
            }
        },
        [selectedSize]
    );

    // Compute whether the product is completely sold out (all sizes have quantity 0)
    const isSoldOut = useMemo(() => {
        if (
            !product ||
            !product.inventory ||
            product.inventory.length === 0
        ) {
            return false;
        }

        return product.inventory.every(
            (item) => item.quantity === 0
        );
    }, [product]);

    const contextValue = useMemo(
        () => ({
            firstImage: product?.firstImage,
            secondImage: product?.secondImage,
            averageRating: product?.averageRating,
            reviews: product?.review,
            productId: product?.id,
            collectionName: product?.collection?.name,
            colorName: product?.color?.name,
            stoneName: product?.stone?.name,
            metalName: product?.metal?.name,
            inventory: product?.inventory,
            relatedProducts: product?.relatedProducts,
            relatedCollectionProducts:
                product?.relatedCollectionProducts,
            loading,
            product,
            selectedSize,
            setSelectedSizeHandler,
            createShoppingBagHandler,
            addToWishlistHandler,
            notSelectedSizeError,
            addToCartError,
            isSoldOut
        }),
        [
            product,
            loading,
            selectedSize,
            createShoppingBagHandler,
            setSelectedSizeHandler,
            addToWishlistHandler,
            notSelectedSizeError,
            addToCartError,
            isSoldOut
        ]
    );

    return (
        <ProductItemContext.Provider value={contextValue}>
            {children}
        </ProductItemContext.Provider>
    );
};
