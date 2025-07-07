import {
    useCallback,
    useMemo,
    useState,
    useEffect,
    useRef
} from 'react';
import { useShoppingBag } from '../api/shoppingBagApi';
import { ShoppingBagContext } from '../contexts/ShoppingBagContext';
import { useNavigate } from 'react-router';

import usePersistedState from '../hooks/usePersistedState';

export const ShoppingBagProvider = ({ children }) => {
    const { deleteItem, getItems, getCount, getTotalPrice, createItem } =
        useShoppingBag();

    const navigate = useNavigate();
    const [isDeleting, setIsDeleting] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const hasInitialized = useRef(false);

    const [shoppingBagItemsCount, setShoppingBagItemsCount] =
        usePersistedState('shopping-bag-count', 0);
    const [shoppingBagTotalPrice, setShoppingBagTotalPrice] =
        usePersistedState('shopping-bag-total-price', 0);
    const [shoppingBagItems, setShoppingBagItems] =
        usePersistedState('shopping-bag-items', []);

    const getShoppingBagItemsHandler = useCallback(async () => {
        setIsLoading(true);
        try {
            const response = await getItems();
            setShoppingBagItems(response);
        } catch {
            // Handle error silently
        } finally {
            setIsLoading(false);
        }
    }, [getItems, setShoppingBagItems]);

    const updateShoppingBagCount = useCallback(async () => {
        try {
            const response = await getCount();
            setShoppingBagItemsCount(response.count);
        } catch {
            // Handle error silently
        }
    }, [getCount, setShoppingBagItemsCount]);

    const updateShoppingBagTotalPrice = useCallback(async () => {
        try {
            const response = await getTotalPrice();
            const price = typeof response.totalPrice === 'string' 
                ? parseFloat(response.totalPrice) 
                : response.totalPrice;
            setShoppingBagTotalPrice(isNaN(price) ? 0 : price);
        } catch {
            // Handle error silently
        }
    }, [getTotalPrice, setShoppingBagTotalPrice]);

    useEffect(() => {
        if (!hasInitialized.current) {
            hasInitialized.current = true;
            getShoppingBagItemsHandler();
            updateShoppingBagCount();
            updateShoppingBagTotalPrice();
        } else {
            hasInitialized.current = false;
            setShoppingBagItems([]);
            setShoppingBagItemsCount(0);
            setShoppingBagTotalPrice(0);
            setIsLoading(false);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const deleteShoppingBagHandler = useCallback(
        async (id) => {
            setIsDeleting(true);
            
            const deletedItem = shoppingBagItems.find(
                (item) => item.id === id
            );
            
            if (!deletedItem) {
                setIsDeleting(false);
                return;
            }
            
            try {
                await deleteItem(id);
                
                const updatedItems = shoppingBagItems.filter(
                    (item) => item.id !== id
                );
                setShoppingBagItems(updatedItems);
                
                const newCount = Math.max(0, shoppingBagItemsCount - deletedItem.quantity);
                setShoppingBagItemsCount(newCount);
                
                setShoppingBagTotalPrice((prev) => {
                    const currentPrice = typeof prev === 'string' ? parseFloat(prev) : prev;
                    const itemPrice = typeof deletedItem.totalPrice === 'string' 
                        ? parseFloat(deletedItem.totalPrice) 
                        : deletedItem.totalPrice;
                    const newPrice = currentPrice - itemPrice;
                    return Math.max(0, isNaN(newPrice) ? 0 : newPrice);
                });
                
            } catch {
                await getShoppingBagItemsHandler();
                await updateShoppingBagCount();
                await updateShoppingBagTotalPrice();
            } finally {
                setIsDeleting(false);
            }
        },
        [
            deleteItem,
            shoppingBagItems,
            shoppingBagItemsCount,
            setShoppingBagItems,
            setShoppingBagItemsCount,
            setShoppingBagTotalPrice,
            getShoppingBagItemsHandler,
            updateShoppingBagCount,
            updateShoppingBagTotalPrice
        ]
    );

    const createShoppingBagItemHandler = useCallback(async (inventory) => {
        try {
            await createItem(inventory);
            await updateShoppingBagCount();
            return { success: true };
        } catch (error) {
            return { success: false, error };
        }
    }, [createItem, updateShoppingBagCount]);

    const continueCheckoutHandler = useCallback(() => {
        navigate('/user/checkout');
    }, [navigate]);

    const refreshShoppingBag = useCallback(async () => {
        await getShoppingBagItemsHandler();
        await updateShoppingBagCount();
        await updateShoppingBagTotalPrice();
    }, [
        getShoppingBagItemsHandler,
        updateShoppingBagCount,
        updateShoppingBagTotalPrice
    ]);

    const contextValue = useMemo(
        () => ({
            shoppingBagItems,
            shoppingBagItemsCount,
            getShoppingBagItemsHandler,
            updateShoppingBagCount,
            shoppingBagTotalPrice,
            deleteShoppingBagHandler,
            isDeleting,
            isLoading,
            updateShoppingBagTotalPrice,
            continueCheckoutHandler,
            refreshShoppingBag,
            createShoppingBagItemHandler
        }),
        [
            continueCheckoutHandler,
            createShoppingBagItemHandler,
            deleteShoppingBagHandler,
            getShoppingBagItemsHandler,
            isDeleting,
            isLoading,
            shoppingBagItems,
            shoppingBagItemsCount,
            shoppingBagTotalPrice,
            updateShoppingBagCount,
            updateShoppingBagTotalPrice,
            refreshShoppingBag
        ]
    );

    return (
        <ShoppingBagContext.Provider value={contextValue}>
            {children}
        </ShoppingBagContext.Provider>
    );
};
