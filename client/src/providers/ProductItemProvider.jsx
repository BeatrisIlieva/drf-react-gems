import { useCallback, useEffect, useMemo, useState } from 'react';

import { useParams } from 'react-router';

import { useProductItem } from '../api/productItemApi';

import { ProductItemContext } from '../contexts/ProductItemContext';
import { useShoppingBagContext } from '../contexts/ShoppingBagContext';

export const ProductItemProvider = ({ children }) => {
    const { getProductItem } = useProductItem();
    const { categoryName, productId } = useParams();
    const { createShoppingBagItemHandler, refreshShoppingBag, shoppingBagItemsCount } =
        useShoppingBagContext();

    const [loading, setLoading] = useState(true);
    const [product, setProduct] = useState(null);
    const [selectedSize, setSelectedSize] = useState(null);
    const [notSelectedSizeError, setNotSelectedSizeError] = useState(null);
    const [selectedInventory, setSelectedInventory] = useState(null);

    const [isMiniBagPopupOpen, setIsMiniBagPopupOpen] = useState(false);

    useEffect(() => {
        const loadProduct = async () => {
            setLoading(true);
            try {
                const response = await getProductItem({
                    categoryName,
                    productId,
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
            const refreshProduct = async () => {
                try {
                    const response = await getProductItem({
                        categoryName,
                        productId,
                    });
                    setProduct(response.product);
                } catch {}
            };
            refreshProduct();
            setIsMiniBagPopupOpen(false);
        } else {
            refreshShoppingBag();
            setIsMiniBagPopupOpen(true);
        }
    }, [isMiniBagPopupOpen, getProductItem, categoryName, productId, refreshShoppingBag]);

    const createShoppingBagHandler = useCallback(async () => {
        if (selectedSize === null) {
            setNotSelectedSizeError(true);
            return;
        }

        try {
            await createShoppingBagItemHandler(selectedInventory);

            if (product && selectedInventory) {
                setProduct(prevProduct => {
                    if (!prevProduct) return null;

                    const updatedProduct = {
                        ...prevProduct,
                        inventory: prevProduct.inventory.map(item => {
                            if (item.id === selectedInventory.objectId) {
                                return {
                                    ...item,
                                    quantity: Math.max(
                                        0,
                                        item.quantity - selectedInventory.quantity
                                    ),
                                };
                            }
                            return item;
                        }),
                    };

                    return updatedProduct;
                });
            }

            setSelectedSize(null);
            setSelectedInventory(null);
            refreshShoppingBag();
            setIsMiniBagPopupOpen(true);
        } catch {}
    }, [
        selectedSize,
        selectedInventory,
        createShoppingBagItemHandler,
        product,
        refreshShoppingBag,
    ]);

    const updateSelectedInventoryHandler = (contentType, objectId) => {
        setSelectedInventory({
            quantity: 1,
            contentType,
            objectId,
        });
    };

    const setSelectedSizeHandler = useCallback(
        (size, contentType, objectId) => {
            if (selectedSize === null) {
                setSelectedSize(size);
                setNotSelectedSizeError(false);
                updateSelectedInventoryHandler(contentType, objectId);
            } else if (selectedSize === size) {
                setSelectedSize(null);
                setNotSelectedSizeError(null);
                setSelectedInventory(null);
            } else {
                setSelectedSize(size);
                setNotSelectedSizeError(false);
                updateSelectedInventoryHandler(contentType, objectId);
            }
        },
        [selectedSize]
    );

    const isSoldOut = useMemo(() => {
        if (!product || !product.inventory || product.inventory.length === 0) {
            return false;
        }

        return product.inventory.every(item => item.quantity === 0);
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
            relatedCollectionProducts: product?.relatedCollectionProducts,
            loading,
            product,
            selectedSize,
            setSelectedSizeHandler,
            createShoppingBagHandler,
            notSelectedSizeError,
            isSoldOut,
            isMiniBagPopupOpen,
            toggleMiniBagPopupOpen,
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
            toggleMiniBagPopupOpen,
        ]
    );

    useEffect(() => {
        if (isMiniBagPopupOpen && shoppingBagItemsCount === 0) {
            const refreshProduct = async () => {
                try {
                    const response = await getProductItem({
                        categoryName,
                        productId,
                    });
                    setProduct(response.product);
                } catch {}
            };
            refreshProduct();
            setIsMiniBagPopupOpen(false);
        }
    }, [shoppingBagItemsCount, isMiniBagPopupOpen, getProductItem, categoryName, productId]);

    return (
        <ProductItemContext.Provider value={contextValue}>{children}</ProductItemContext.Provider>
    );
};
