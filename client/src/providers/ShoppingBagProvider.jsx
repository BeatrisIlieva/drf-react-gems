import { useCallback, useContext, useEffect, useMemo, useState } from 'react';

import { useNavigate } from 'react-router';

import { useShoppingBag } from '../api/shoppingBagApi';

import { useGuest } from '../hooks/useGuest';
import usePersistedState from '../hooks/usePersistedState';

import { ShoppingBagContext } from '../contexts/ShoppingBagContext';
import { UserContext } from '../contexts/UserContext';

export const ShoppingBagProvider = ({ children }) => {
    const { deleteItem, getItems, getCount, getTotalPrice, createItem } = useShoppingBag();
    const { id: userId, access } = useContext(UserContext);
    const { getGuestData } = useGuest();
    const guestId = getGuestData();

    const navigate = useNavigate();
    const [isDeleting, setIsDeleting] = useState(false);
    const [loading, setLoading] = useState(true);

    const [shoppingBagItemsCount, setShoppingBagItemsCount] = usePersistedState(
        'shopping-bag-count',
        0
    );
    const [shoppingBagTotalPrice, setShoppingBagTotalPrice] = usePersistedState(
        'shopping-bag-total-price',
        0
    );
    const [shoppingBagItems, setShoppingBagItems] = usePersistedState('shopping-bag-items', []);

    const [isMiniBagPopupOpen, setIsMiniBagPopupOpen] = useState(false);
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
        let mounted = true;

        const loadShoppingBag = async () => {
            if (!userId && !guestId) {
                setShoppingBagItems([]);
                setShoppingBagItemsCount(0);
                setShoppingBagTotalPrice(0);
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
        guestId,
        getItems,
        getCount,
        getTotalPrice,
        setShoppingBagItems,
        setShoppingBagItemsCount,
        setShoppingBagTotalPrice,
    ]);

    const deleteShoppingBagHandler = useCallback(
        async id => {
            setIsDeleting(true);

            const deletedItem = shoppingBagItems.find(item => item.id === id);

            if (!deletedItem) {
                setIsDeleting(false);
                return;
            }

            try {
                await deleteItem(id);

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
        [deleteItem, shoppingBagItems, shoppingBagItemsCount, getItems, getCount, getTotalPrice]
    );

    const createShoppingBagItemHandler = useCallback(
        async inventory => {
            try {
                await createItem(inventory);

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
        [createItem, getItems, getCount, getTotalPrice]
    );

    const continueCheckoutHandler = useCallback(() => {
        closeMiniBagPopup();

        if (!access) {
            navigate('/my-account/login?next=/user/checkout');
        } else {
            navigate('/user/checkout');
        }
    }, [navigate, access, closeMiniBagPopup]);

    const refreshShoppingBag = useCallback(async () => {
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
    }, [getItems, getCount, getTotalPrice]);

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
