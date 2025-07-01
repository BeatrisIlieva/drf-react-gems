import { useCallback, useMemo, useState } from 'react';
import { useShoppingBag } from '../api/shoppingBagApi';
import { ShoppingBagContext } from '../contexts/ShoppingBagContext';
import { useNavigate } from 'react-router';
import { useAuth } from '../hooks/auth/useAuth';

export const ShoppingBagProvider = ({ children }) => {
    const { deleteItem, getItems, getCount, getTotalPrice } =
        useShoppingBag();

    const { isAuthenticated } = useAuth();
    const navigate = useNavigate();
    const [isDeleting, setIsDeleting] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    const [shoppingBagItemsCount, setShoppingBagItemsCount] =
        useState(0);
    const [shoppingBagTotalPrice, setShoppingBagTotalPrice] =
        useState(0);
    const [shoppingBagItems, setShoppingBagItems] = useState([]);

    const getShoppingBagItemsHandler = useCallback(async () => {
        setIsLoading(true);
        try {
            const response = await getItems();
            if (response) {
                setShoppingBagItems(response);
            }
        } catch (err) {
            console.error(
                'Error fetching shopping bag items:',
                err instanceof Error ? err.message : String(err)
            );
        } finally {
            setIsLoading(false);
        }
    }, [getItems]);

    const updateShoppingBagCount = useCallback(async () => {
        try {
            const response = await getCount();
            if (response) {
                setShoppingBagItemsCount(response.count);
            }
        } catch (err) {
            console.error(
                'Error updating shopping bag count:',
                err instanceof Error ? err.message : String(err)
            );
        }
    }, [getCount]);

    const updateShoppingBagTotalPrice = useCallback(async () => {
        try {
            const response = await getTotalPrice();
            if (response) {
                setShoppingBagTotalPrice(response.totalPrice);
            }
        } catch (err) {
            console.error(
                'Error updating shopping bag total price:',
                err instanceof Error ? err.message : String(err)
            );
        }
    }, [getTotalPrice]);

    const deleteShoppingBagHandler = useCallback(
        async (id) => {
            setIsDeleting(true);
            try {
                await deleteItem(id);

                // Immediately update local state to reflect the deletion
                const updatedItems = shoppingBagItems.filter(
                    (item) => item.id !== id
                );
                setShoppingBagItems(updatedItems);

                // Optimistically update the count
                setShoppingBagItemsCount((prev) =>
                    Math.max(0, prev - 1)
                );

                // Calculate and update the total price optimistically
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

                // Also fetch the latest data from the server to ensure consistency
                Promise.all([
                    getCount().then((response) => {
                        if (response) {
                            setShoppingBagItemsCount(
                                response.count
                            );
                        }
                    }),
                    getTotalPrice().then((response) => {
                        if (response) {
                            setShoppingBagTotalPrice(
                                response.totalPrice
                            );
                        }
                    })
                ]).catch((err) => {
                    console.error(
                        'Error updating shopping bag data after deletion:',
                        err instanceof Error
                            ? err.message
                            : String(err)
                    );
                });
            } catch (error) {
                console.error(
                    'Error deleting shopping bag item:',
                    error instanceof Error
                        ? error.message
                        : String(error)
                );

                // Fallback: refresh all data in case of error
                getShoppingBagItemsHandler();
            } finally {
                setIsDeleting(false);
            }
        },
        [
            deleteItem,
            getCount,
            getShoppingBagItemsHandler,
            getTotalPrice,
            shoppingBagItems
        ]
    );

    const continueCheckoutHandler = useCallback(() => {
        if (!isAuthenticated) {
            navigate('/my-account/login');
            return;
        }

        navigate('/checkout');
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
