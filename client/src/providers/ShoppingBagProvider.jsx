import { useCallback, useEffect, useMemo, useState } from 'react';

import { useNavigate } from 'react-router';

import { useShoppingBag } from '../api/shoppingBagApi';

import usePersistedState from '../hooks/usePersistedState';

import { ShoppingBagContext } from '../contexts/ShoppingBagContext';
import { useUserContext } from '../contexts/UserContext';

import { createBagItem } from '../utils/createBagItem';

export const ShoppingBagProvider = ({ children }) => {
    const { deleteItem, getItems, getCount, getTotalPrice, createItem } = useShoppingBag();
    const { access } = useUserContext();
    const authData = JSON.parse(localStorage.getItem('auth'));
    const userId = authData?.id;
    const navigate = useNavigate();
    const migratedItemsData = JSON.parse(localStorage.getItem('migratedShoppingBag'));
    const migratedItems = migratedItemsData;

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

    const loadShoppingBag = useCallback(async () => {
        setLoading(true);
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

            return { success: true };
        } catch {
            setShoppingBagItems([]);
            setShoppingBagItemsCount(0);
            setShoppingBagTotalPrice(0);
        } finally {
            setLoading(false);
        }
    }, [
        getCount,
        getItems,
        getTotalPrice,
        setShoppingBagItems,
        setShoppingBagItemsCount,
        setShoppingBagTotalPrice,
    ]);

    const migrateItemsToShoppingBag = useCallback(async () => {
        for (const item of shoppingBagItems) {
            await createItem({ inventory: item.id, quantity: item.quantity });
        }
    }, [createItem, shoppingBagItems]);

    useEffect(() => {
        if (userId && !migratedItems) {
            migrateItemsToShoppingBag().then(() => {
                localStorage.setItem('migratedShoppingBag', true);
                loadShoppingBag();
            });
        }
    }, [
        userId,
        createItem,
        shoppingBagItems,
        migratedItems,
        loadShoppingBag,
        migrateItemsToShoppingBag,
    ]);

    useEffect(() => {
        if (!userId) {
            setShoppingBagItems([]);
            setShoppingBagItemsCount(0);
            setShoppingBagTotalPrice(0);
            setLoading(false);
            return;
        }

        loadShoppingBag();
    }, [
        userId,
        setShoppingBagItems,
        setShoppingBagItemsCount,
        setShoppingBagTotalPrice,
        loadShoppingBag,
    ]);

    // useEffect(() => {
    //     if (!userId) {
    //         return;
    //     }
    //     loadShoppingBag();
    // }, [loadShoppingBag, userId]);

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

                loadShoppingBag();
            } catch (error) {
                return { success: false, error };
            }
        },
        [createItem, setShoppingBagItems, shoppingBagItems, userId, loadShoppingBag]
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

            await loadShoppingBag();
        },
        [setShoppingBagItems, shoppingBagItems, userId, loadShoppingBag]
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
