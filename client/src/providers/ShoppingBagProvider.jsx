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
import { useAuth } from '../hooks/auth/useAuth';
import usePersistedState from '../hooks/usePersistedState';

export const ShoppingBagProvider = ({ children }) => {
    const { deleteItem, getItems, getCount, getTotalPrice } =
        useShoppingBag();

    const { isAuthenticated } = useAuth();
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
        if (!isAuthenticated) return;

        setIsLoading(true);
        try {
            const response = await getItems();
            setShoppingBagItems(response);
        } catch (err) {
            console.error(err.message);
        } finally {
            setIsLoading(false);
        }
    }, [getItems, isAuthenticated, setShoppingBagItems]);

    const updateShoppingBagCount = useCallback(async () => {
        if (!isAuthenticated) return;

        try {
            const response = await getCount();
            setShoppingBagItemsCount(response.count);
        } catch (err) {
            console.error(err.message);
        }
    }, [getCount, isAuthenticated, setShoppingBagItemsCount]);

    const updateShoppingBagTotalPrice = useCallback(async () => {
        if (!isAuthenticated) return;

        try {
            const response = await getTotalPrice();
            setShoppingBagTotalPrice(response.totalPrice);
        } catch (err) {
            console.error(err.message);
        }
    }, [
        getTotalPrice,
        isAuthenticated,
        setShoppingBagTotalPrice
    ]);

    useEffect(() => {
        if (isAuthenticated && !hasInitialized.current) {
            hasInitialized.current = true;
            getShoppingBagItemsHandler();
            updateShoppingBagCount();
            updateShoppingBagTotalPrice();
        } else if (!isAuthenticated) {
            hasInitialized.current = false;
            setShoppingBagItems([]);
            setShoppingBagItemsCount(0);
            setShoppingBagTotalPrice(0);
            setIsLoading(false);
        }
    }, [
        isAuthenticated,
        getShoppingBagItemsHandler,
        updateShoppingBagCount,
        updateShoppingBagTotalPrice,
        setShoppingBagItems,
        setShoppingBagItemsCount,
        setShoppingBagTotalPrice
    ]);

    const deleteShoppingBagHandler = useCallback(
        async (id) => {
            setIsDeleting(true);
            try {
                await deleteItem(id);

                const updatedItems = shoppingBagItems.filter(
                    (item) => item.id !== id
                );
                setShoppingBagItems(updatedItems);

                setShoppingBagItemsCount((prev) =>
                    Math.max(0, prev - 1)
                );

                const deletedItem = shoppingBagItems.find(
                    (item) => item.id === id
                );
                if (deletedItem) {
                    setShoppingBagTotalPrice((prev) =>
                        Math.max(
                            0,
                            prev -
                                deletedItem.totalPricePerProduct
                        )
                    );
                }
            } catch (error) {
                console.error(
                    'Error deleting shopping bag item:',
                    error instanceof Error
                        ? error.message
                        : String(error)
                );

                getShoppingBagItemsHandler();
            } finally {
                setIsDeleting(false);
            }
        },
        [
            deleteItem,
            getShoppingBagItemsHandler,
            shoppingBagItems,
            setShoppingBagItems,
            setShoppingBagItemsCount,
            setShoppingBagTotalPrice
        ]
    );

    const continueCheckoutHandler = useCallback(() => {
        if (!isAuthenticated) {
            navigate('/my-account/login');
            return;
        }

        navigate('/user/checkout');
    }, [isAuthenticated, navigate]);

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
            continueCheckoutHandler
        }),
        [
            continueCheckoutHandler,
            deleteShoppingBagHandler,
            getShoppingBagItemsHandler,
            isDeleting,
            isLoading,
            shoppingBagItems,
            shoppingBagItemsCount,
            shoppingBagTotalPrice,
            updateShoppingBagCount,
            updateShoppingBagTotalPrice
        ]
    );

    return (
        <ShoppingBagContext.Provider value={contextValue}>
            {children}
        </ShoppingBagContext.Provider>
    );
};
