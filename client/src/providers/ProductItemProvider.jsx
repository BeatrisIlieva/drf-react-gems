import { useParams } from 'react-router';
import { useProductItem } from '../api/products/productItemApi';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { ProductItemContext } from '../contexts/ProductItemContext';
import { useShoppingBagContext } from '../contexts/ShoppingBagContext';

export const ProductItemProvider = ({ children }) => {
    const { getProductItem } = useProductItem();
    const { categoryName, productId } = useParams();
    const {
        createShoppingBagItemHandler,
        getShoppingBagItemsHandler,
        shoppingBagItemsCount
    } = useShoppingBagContext();

    const [loading, setLoading] = useState(true);
    const [product, setProduct] = useState(null);
    const [selectedSize, setSelectedSize] = useState(null);
    const [notSelectedSizeError, setNotSelectedSizeError] =
        useState(null);
    const [selectedInventory, setSelectedInventory] =
        useState(null);

    const [isMiniBagPopupOpen, setIsMiniBagPopupOpen] =
        useState(false);

    useEffect(() => {
        const loadProduct = async () => {
            setLoading(true);
            try {
                const response = await getProductItem({
                    categoryName,
                    productId
                });
                setProduct(response.product);
            } finally {
                setLoading(false);
            }
        };

        loadProduct();
    }, [categoryName, productId, getProductItem]);

    const toggleMiniBagPopupOpen = useCallback(() => {
        if (isMiniBagPopupOpen) {
            // When closing the popup, refresh the product data to update inventory
            const refreshProduct = async () => {
                try {
                    const response = await getProductItem({
                        categoryName,
                        productId
                    });
                    setProduct(response.product);
                } catch {
                    // Silently handle errors
                }
            };
            refreshProduct();
            setIsMiniBagPopupOpen(false);
        } else {
            getShoppingBagItemsHandler();
            setIsMiniBagPopupOpen(true);
        }
    }, [isMiniBagPopupOpen, getProductItem, categoryName, productId, getShoppingBagItemsHandler]);

    const createShoppingBagHandler = useCallback(async () => {
        if (selectedSize === null) {
            setNotSelectedSizeError(true);
            return;
        }

        try {
            await createShoppingBagItemHandler(selectedInventory);

            if (product && selectedInventory) {
                setProduct((prevProduct) => {
                    if (!prevProduct) return null;

                    const updatedProduct = {
                        ...prevProduct,
                        inventory: prevProduct.inventory.map(
                            (item) => {
                                if (
                                    item.id ===
                                    selectedInventory.objectId
                                ) {
                                    return {
                                        ...item,
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

            setSelectedSize(null);
            setSelectedInventory(null);
            getShoppingBagItemsHandler();
            setIsMiniBagPopupOpen(true);
        } catch {
            // No error message shown to user
        }
    }, [
        selectedSize,
        selectedInventory,
        createShoppingBagItemHandler,
        product,
        getShoppingBagItemsHandler
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
            notSelectedSizeError,
            isSoldOut,
            isMiniBagPopupOpen,
            toggleMiniBagPopupOpen
        }),
        [
            product,
            loading,
            selectedSize,
            createShoppingBagHandler,
            setSelectedSizeHandler,
            notSelectedSizeError,
            isSoldOut,
            isMiniBagPopupOpen,
            toggleMiniBagPopupOpen
        ]
    );

    // Automatically close the mini shopping bag popup when it becomes empty
    useEffect(() => {
        if (isMiniBagPopupOpen && shoppingBagItemsCount === 0) {
            // Only refresh product if we're closing due to empty bag
            const refreshProduct = async () => {
                try {
                    const response = await getProductItem({
                        categoryName,
                        productId
                    });
                    setProduct(response.product);
                } catch {
                    // Silently handle errors
                }
            };
            refreshProduct();
            setIsMiniBagPopupOpen(false);
        }
    }, [shoppingBagItemsCount, isMiniBagPopupOpen, getProductItem, categoryName, productId]);

    return (
        <ProductItemContext.Provider value={contextValue}>
            {children}
        </ProductItemContext.Provider>
    );
};
