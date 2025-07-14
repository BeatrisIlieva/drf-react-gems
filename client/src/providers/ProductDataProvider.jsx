import { useCallback, useEffect, useMemo, useState } from 'react';

import { useParams } from 'react-router';

import { useProductItem } from '../api/productItemApi';

import { ProductItemContext } from '../contexts/ProductItemContext';
import { useShoppingBagContext } from '../contexts/ShoppingBagContext';

export const ProductDataProvider = ({
    children,

    productData = null,
    categoryName: propCategoryName = null,
    productId: propProductId = null,
}) => {
    const { getProductItem } = useProductItem();
    const { categoryName: urlCategoryName, productId: urlProductId } = useParams();
    const {
        createShoppingBagItemHandler,
        refreshShoppingBag,
        shoppingBagItemsCount,
        openMiniBagPopup,
    } = useShoppingBagContext();

    const categoryName = propCategoryName || urlCategoryName;
    const productId = propProductId || urlProductId;

    const [loading, setLoading] = useState(true);
    const [product, setProduct] = useState(productData);
    const [selectedSize, setSelectedSize] = useState(null);
    const [notSelectedSizeError, setNotSelectedSizeError] = useState(null);
    const [selectedInventory, setSelectedInventory] = useState(null);

    useEffect(() => {
        const loadProduct = async () => {
            if (productData) {
                setProduct(productData);
                setLoading(false);
                return;
            }

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
    }, [categoryName, productId, getProductItem, productData]);

    const createShoppingBagHandler = useCallback(async () => {
        if (selectedSize === null) {
            setNotSelectedSizeError(true);

            return false;
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
            openMiniBagPopup();

            return true;
        } catch (error) {
            return false;
        }
    }, [
        selectedSize,
        selectedInventory,
        createShoppingBagItemHandler,
        product,
        refreshShoppingBag,
        openMiniBagPopup,
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

    const refreshProduct = useCallback(async () => {
        try {
            const response = await getProductItem({
                categoryName,
                productId,
            });
            setProduct(response.product);
        } catch {}
    }, [getProductItem, categoryName, productId]);

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
            relatedProducts: product?.relatedProducts || [],
            relatedCollectionProducts: product?.relatedCollectionProducts || [],
            loading,
            product,
            selectedSize,
            setSelectedSizeHandler,
            createShoppingBagHandler,
            notSelectedSizeError,
            isSoldOut,
            refreshProduct,
        }),
        [
            product,
            loading,
            selectedSize,
            createShoppingBagHandler,
            setSelectedSizeHandler,
            notSelectedSizeError,
            isSoldOut,
            refreshProduct,
        ]
    );

    useEffect(() => {
        if (productData) {
            return;
        }

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
    }, [shoppingBagItemsCount, getProductItem, categoryName, productId, productData]);

    return (
        <ProductItemContext.Provider value={contextValue}>{children}</ProductItemContext.Provider>
    );
};
