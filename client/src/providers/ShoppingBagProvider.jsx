import { useCallback, useEffect, useMemo, useState } from 'react';

import { useNavigate } from 'react-router';

import { useShoppingBag } from '../api/shoppingBagApi';

import usePersistedState from '../hooks/usePersistedState';

import { ShoppingBagContext } from '../contexts/ShoppingBagContext';
import { useUserContext } from '../contexts/UserContext';

import { createBagItem } from '../utils/createBagItem';

export const ShoppingBagProvider = ({ children }) => {
    const { deleteItem, getItems, getCount, getTotalPrice, createItem } = useShoppingBag();
    const { id: userId, access } = useUserContext();
    const navigate = useNavigate();

    const [shouldReload, setShouldReload] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [loading, setLoading] = useState(true);
    const [isMiniBagPopupOpen, setIsMiniBagPopupOpen] = useState(false);

    const [shoppingBagItemsCount, setShoppingBagItemsCount] = usePersistedState(
        'shopping-bag-count',
        0
    );
    const [shoppingBagTotalPrice, setShoppingBagTotalPrice] = usePersistedState(
        'shopping-bag-total-price',
        0
    );
    const [shoppingBagItems, setShoppingBagItems] = usePersistedState('shopping-bag-items', []);

    const toggleMiniBagPopupOpen = useCallback(() => {
        setIsMiniBagPopupOpen(prev => !prev);
    }, []);
    const openMiniBagPopup = useCallback(() => {
        setIsMiniBagPopupOpen(true);
    }, []);
    const closeMiniBagPopup = useCallback(() => setIsMiniBagPopupOpen(false), []);

    useEffect(() => {}, [isMiniBagPopupOpen]);

    useEffect(() => {
        if (shoppingBagItemsCount === 0 && isMiniBagPopupOpen) {
            closeMiniBagPopup();
        }
    }, [shoppingBagItemsCount, isMiniBagPopupOpen, closeMiniBagPopup]);

    useEffect(() => {
        if (shoppingBagItems.length > 0 && userId) {
            for (const item of shoppingBagItems) {
                createItem({ inventory: item.id, quantity: item.quantity });
            }

            setShouldReload(true);
        }
    }, [userId]);

    useEffect(() => {
        if (!userId) {
            setShoppingBagItems([]);
            setShoppingBagItemsCount(0);
            setShoppingBagTotalPrice(0);
        }
    }, [userId, setShoppingBagItems, setShoppingBagItemsCount, setShoppingBagTotalPrice]);

    useEffect(() => {
        let mounted = true;

        const loadShoppingBag = async () => {
            if (!userId) {
                setLoading(false);
                return;
            }

            setLoading(true);
            try {
                const [itemsResponse, countResponse, priceResponse] = await Promise.all([
                    getItems(),
                    getCount(),
                    getTotalPrice(),
                ]);

                if (mounted) {
                    setShoppingBagItems(itemsResponse);
                    setShoppingBagItemsCount(countResponse.count);

                    const price =
                        typeof priceResponse.totalPrice === 'string'
                            ? parseFloat(priceResponse.totalPrice)
                            : priceResponse.totalPrice;
                    setShoppingBagTotalPrice(isNaN(price) ? 0 : price);
                }
            } catch {
                if (mounted) {
                    setShoppingBagItems([]);
                    setShoppingBagItemsCount(0);
                    setShoppingBagTotalPrice(0);
                }
            } finally {
                if (mounted) {
                    setLoading(false);
                }
            }
        };

        loadShoppingBag();

        return () => {
            mounted = false;
        };
    }, [
        userId,
        getItems,
        getCount,
        getTotalPrice,
        setShoppingBagItems,
        setShoppingBagItemsCount,
        setShoppingBagTotalPrice,
        shouldReload,
    ]);

    useEffect(() => {
        setShoppingBagItemsCount(
            Array.isArray(shoppingBagItems)
                ? shoppingBagItems.reduce((sum, item) => sum + (item.quantity || 0), 0)
                : 0
        );
    }, [shoppingBagItems, setShoppingBagItemsCount]);

    useEffect(() => {
        setShoppingBagTotalPrice(
            Array.isArray(shoppingBagItems)
                ? shoppingBagItems.reduce(
                      (sum, item) =>
                          sum +
                          (typeof item.totalPrice === 'string'
                              ? parseFloat(item.totalPrice)
                              : item.totalPrice || 0),
                      0
                  )
                : 0
        );
    }, [shoppingBagItems, setShoppingBagTotalPrice]);

    const deleteShoppingBagHandler = useCallback(
        async id => {
            setIsDeleting(true);

            const deletedItem = shoppingBagItems.find(item => item.id === id);

            if (!deletedItem) {
                setIsDeleting(false);
                return;
            }

            try {
                if (userId) {
                    await deleteItem(id);
                }

                const updatedItems = shoppingBagItems.filter(item => item.id !== id);
                setShoppingBagItems(updatedItems);

                const newCount = Math.max(0, shoppingBagItemsCount - deletedItem.quantity);
                setShoppingBagItemsCount(newCount);

                setShoppingBagTotalPrice(prev => {
                    const currentPrice = typeof prev === 'string' ? parseFloat(prev) : prev;
                    const itemPrice =
                        typeof deletedItem.totalPrice === 'string'
                            ? parseFloat(deletedItem.totalPrice)
                            : deletedItem.totalPrice;
                    const newPrice = currentPrice - itemPrice;
                    return Math.max(0, isNaN(newPrice) ? 0 : newPrice);
                });
            } catch {
                const loadShoppingBag = async () => {
                    try {
                        const response = await getItems();
                        setShoppingBagItems(response);
                        const countResponse = await getCount();
                        setShoppingBagItemsCount(countResponse.count);
                        const priceResponse = await getTotalPrice();
                        const price =
                            typeof priceResponse.totalPrice === 'string'
                                ? parseFloat(priceResponse.totalPrice)
                                : priceResponse.totalPrice;
                        setShoppingBagTotalPrice(isNaN(price) ? 0 : price);
                    } catch {}
                };
                await loadShoppingBag();
            } finally {
                setIsDeleting(false);
            }
        },
        [
            deleteItem,
            shoppingBagItems,
            shoppingBagItemsCount,
            getItems,
            getCount,
            getTotalPrice,
            setShoppingBagItems,
            setShoppingBagItemsCount,
            setShoppingBagTotalPrice,
            userId,
        ]
    );

    const createShoppingBagItemHandler = useCallback(
        async (inventoryInput, product, categoryName) => {
            if (!userId) {
                const itemAlreadyAdded = shoppingBagItems.find(
                    item => Number(item.id) === Number(inventoryInput.inventory)
                );

                if (itemAlreadyAdded) {
                    setShoppingBagItems(prev =>
                        prev.map(item =>
                            item.id === itemAlreadyAdded.id
                                ? {
                                      ...item,
                                      quantity: item.quantity + 1,
                                      totalPrice: item.totalPrice + item.productInfo.price,
                                  }
                                : item
                        )
                    );
                } else {
                    const category = categoryName.charAt(0).toUpperCase() + categoryName.slice(1);
                    const data = createBagItem(product, inventoryInput, category);
                    setShoppingBagItems(prev => [data, ...prev]);
                }

                return { success: true };
            }
            let inventory, quantity;
            if (typeof inventoryInput === 'object' && inventoryInput !== null) {
                inventory = inventoryInput.inventory || inventoryInput.id || inventoryInput;
                quantity = inventoryInput.quantity || 1;
            } else {
                inventory = inventoryInput;
                quantity = 1;
            }
            try {
                await createItem({ inventory, quantity });

                const [itemsResponse, countResponse, priceResponse] = await Promise.all([
                    getItems(),
                    getCount(),
                    getTotalPrice(),
                ]);

                setShoppingBagItems(itemsResponse);
                setShoppingBagItemsCount(countResponse.count);

                const price =
                    typeof priceResponse.totalPrice === 'string'
                        ? parseFloat(priceResponse.totalPrice)
                        : priceResponse.totalPrice;
                setShoppingBagTotalPrice(isNaN(price) ? 0 : price);

                return { success: true };
            } catch (error) {
                return { success: false, error };
            }
        },
        [
            createItem,
            getItems,
            getCount,
            getTotalPrice,
            setShoppingBagItems,
            setShoppingBagItemsCount,
            setShoppingBagTotalPrice,
            shoppingBagItems,
            userId,
        ]
    );

    const continueCheckoutHandler = useCallback(() => {
        closeMiniBagPopup();

        if (!access) {
            navigate('/my-account/login?next=/user/checkout');
        } else {
            navigate('/user/checkout');
        }
    }, [navigate, access, closeMiniBagPopup]);

    const refreshShoppingBag = useCallback(
        async (id = null, localQuantity = null) => {
            if (!userId) {
                const itemAlreadyAdded = shoppingBagItems.find(
                    item => Number(item.id) === Number(id)
                );

                if (localQuantity === 0) {
                    setShoppingBagItems(prev => prev.filter(item => item.id !== id));
                    return;
                }

                if (itemAlreadyAdded) {
                    setShoppingBagItems(prev =>
                        prev.map(item =>
                            item.id === itemAlreadyAdded.id
                                ? {
                                      ...item,
                                      quantity: localQuantity,
                                      totalPrice: item.productInfo.price * localQuantity,
                                  }
                                : item
                        )
                    );
                }
                return;
            }
            try {
                const [itemsResponse, countResponse, priceResponse] = await Promise.all([
                    getItems(),
                    getCount(),
                    getTotalPrice(),
                ]);

                setShoppingBagItems(itemsResponse);
                setShoppingBagItemsCount(countResponse.count);

                const price =
                    typeof priceResponse.totalPrice === 'string'
                        ? parseFloat(priceResponse.totalPrice)
                        : priceResponse.totalPrice;
                setShoppingBagTotalPrice(isNaN(price) ? 0 : price);
            } catch {
                setShoppingBagItems([]);
                setShoppingBagItemsCount(0);
                setShoppingBagTotalPrice(0);
            }
        },
        [
            getItems,
            getCount,
            getTotalPrice,
            setShoppingBagItems,
            setShoppingBagItemsCount,
            setShoppingBagTotalPrice,
            shoppingBagItems,
            userId,
        ]
    );

    const contextValue = useMemo(
        () => ({
            shoppingBagItems,
            shoppingBagItemsCount,
            shoppingBagTotalPrice,
            deleteShoppingBagHandler,
            isDeleting,
            loading,
            continueCheckoutHandler,
            refreshShoppingBag,
            createShoppingBagItemHandler,
            isMiniBagPopupOpen,
            toggleMiniBagPopupOpen,
            openMiniBagPopup,
            closeMiniBagPopup,
        }),
        [
            continueCheckoutHandler,
            createShoppingBagItemHandler,
            deleteShoppingBagHandler,
            isDeleting,
            loading,
            shoppingBagItems,
            shoppingBagItemsCount,
            shoppingBagTotalPrice,
            refreshShoppingBag,
            isMiniBagPopupOpen,
            toggleMiniBagPopupOpen,
            openMiniBagPopup,
            closeMiniBagPopup,
        ]
    );

    return (
        <ShoppingBagContext.Provider value={contextValue}>{children}</ShoppingBagContext.Provider>
    );
};
