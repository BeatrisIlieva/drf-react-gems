import { use, useCallback, useEffect, useMemo, useState } from 'react';

import { useParams } from 'react-router';

import { useProductItem } from '../api/productItemApi';

import { ProductItemContext } from '../contexts/ProductItemContext';
import { useShoppingBagContext } from '../contexts/ShoppingBagContext';
import { useUserContext } from '../contexts/UserContext';

export const ProductDataProvider = ({
    children,

    productData = null,
    categoryName: propCategoryName = null,
    productId: propProductId = null,
}) => {
    const { getProductItem } = useProductItem();
    const { categoryName: urlCategoryName, productId: urlProductId } = useParams();
    const { id: userId } = useUserContext();
    const {
        createShoppingBagItemHandler,
        refreshShoppingBag,
        shoppingBagItemsCount,
        openMiniBagPopup,
        shoppingBagItems,
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

    const updateSelectedInventoryHandler = inventoryId => {
        setSelectedInventory({
            quantity: 1,
            inventory: inventoryId,
        });
    };

    const setSelectedSizeHandler = useCallback(
        (size, inventoryId) => {
            if (selectedSize === null) {
                setSelectedSize(size);
                setNotSelectedSizeError(false);
                updateSelectedInventoryHandler(inventoryId);
            } else if (selectedSize === size) {
                setSelectedSize(null);
                setNotSelectedSizeError(null);
                setSelectedInventory(null);
            } else {
                setSelectedSize(size);
                setNotSelectedSizeError(false);
                updateSelectedInventoryHandler(inventoryId);
            }
        },
        [selectedSize]
    );

    const createShoppingBagHandler = useCallback(async () => {
        if (selectedSize === null) {
            setNotSelectedSizeError(true);
            return false;
        }
        try {
            await createShoppingBagItemHandler(selectedInventory, product, categoryName);
            if (product && selectedInventory) {
                setProduct(prevProduct => {
                    if (!prevProduct) return null;
                    const updatedProduct = {
                        ...prevProduct,
                        inventory: prevProduct.inventory.map(item => {
                            if (item.id === selectedInventory.inventory) {
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
        categoryName
    ]);

    useEffect(() => {
        setSelectedSize(null);
        setNotSelectedSizeError(false);
        setSelectedInventory(null);
    }, [productId, categoryName]);

    const isSoldOut = useMemo(() => {
        if (!product || !product.inventory) return false;

        const result = product.inventory.every(item => {
            return (
                item.quantity ===
                shoppingBagItems.filter(
                    bagItem => bagItem.id === item.id || bagItem.inventory === item.id
                )[0]?.quantity
            );
        });

        return result;
    }, [product, shoppingBagItems]);

    const refreshProduct = useCallback(async () => {
        if (!userId) return;
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
