import { useParams } from 'react-router';
import { useProductItem } from '../api/productItemApi';
import type { ProductItemType } from '../types/Products';
import {
    useCallback,
    useEffect,
    useMemo,
    useState,
    type ReactNode
} from 'react';
import { ProductItemContext } from '../contexts/ProductItemContext';
import { useCreateShoppingBag } from '../api/shoppingBagApi';
import type { CreateShoppingBagParams } from '../types/ShoppingBag';

interface Props {
    children: ReactNode;
}

export const ProductItemProvider = ({ children }: Props) => {
    const { getProductItem } = useProductItem();
    const { categoryName, productId } = useParams<{
        categoryName: string;
        productId: string;
    }>();
    const { createShoppingBag } = useCreateShoppingBag();

    const [loading, setLoading] = useState<boolean>(true);
    const [product, setProduct] =
        useState<ProductItemType | null>(null);
    const [selectedSize, setSelectedSize] = useState<
        number | null
    >(null);
    const [notSelectedSizeError, setNotSelectedSizeError] =
        useState<boolean | null>(null);
    const [selectedInventory, setSelectedInventory] =
        useState<CreateShoppingBagParams | null>(null);
    const [addToCartError, setAddToCartError] = useState<
        string | null
    >(null);

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

        // Set up a polling mechanism to refresh product data periodically
        // Only update if the user is actively viewing the product (not typing/navigating away)
        const pollInterval = 1000;
        const pollTimer = setInterval(() => {
            // Silently refresh data without showing loading indicators
            const refreshProductData = async () => {
                try {
                    const response = await getProductItem({
                        categoryName,
                        productId
                    });
                    // Only update if there's a significant change in inventory to avoid unnecessary re-renders
                    setProduct((prevProduct) => {
                        if (!prevProduct) return response.product;

                        // Check if inventory structure has changed significantly
                        const hasInventoryStructureChanged = 
                            prevProduct.inventory.length !== response.product.inventory.length;
                        
                        // If structure hasn't changed, check if any available items have become unavailable
                        // or if any unavailable items have become available (ignoring quantity changes for already available items)
                        if (!hasInventoryStructureChanged) {
                            const hasAvailabilityChanged = prevProduct.inventory.some((prevItem, index) => {
                                const newItem = response.product.inventory[index];
                                // Check if an item has gone from available to unavailable or vice versa
                                return (prevItem.quantity > 0 && newItem.quantity === 0) || 
                                       (prevItem.quantity === 0 && newItem.quantity > 0);
                            });
                            
                            // Only update if availability has changed
                            return hasAvailabilityChanged ? response.product : prevProduct;
                        }
                        
                        return response.product;
                    });
                } catch (error) {
                    // Silent fail - doesn't update UI on polling errors
                    console.debug(
                        'Background refresh failed:',
                        error
                    );
                }
            };

            refreshProductData();
        }, pollInterval);

        // Clean up the interval when component unmounts or params change
        return () => clearInterval(pollTimer);
    }, [
        categoryName,
        productId,
        getProductItem,
        getProductItemHandler
    ]);

    const createShoppingBagHandler =
        useCallback(async (): Promise<void> => {
            if (selectedSize === null) {
                setNotSelectedSizeError(true);
                return;
            }

            setAddToCartError(null);
            try {
                await createShoppingBag(selectedInventory!);

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
            createShoppingBag,
            selectedInventory,
            product,
            getProductItemHandler
        ]);

    const addToWishlistHandler = (): void => {};

    const updateSelectedInventoryHandler = (
        contentType: string,
        objectId: number
    ) => {
        setSelectedInventory({
            quantity: 1,
            contentType,
            objectId
        });
    };

    const setSelectedSizeHandler = useCallback(
        (
            size: number,
            contentType: string,
            objectId: number
        ): void => {
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
