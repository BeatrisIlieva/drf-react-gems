import { useCallback, useMemo, useState, useEffect, useContext } from "react";
import { useShoppingBag } from "../api/shoppingBagApi";
import { ShoppingBagContext } from "../contexts/ShoppingBagContext";
import { UserContext } from "../contexts/UserContext";
import { useNavigate } from "react-router";

export const ShoppingBagProvider = ({ children }) => {
    const { deleteItem, getItems, getCount, getTotalPrice, createItem } =
        useShoppingBag();
    const { id: userId } = useContext(UserContext);

    const navigate = useNavigate();
    const [isDeleting, setIsDeleting] = useState(false);
    const [loading, setLoading] = useState(true);

    const [shoppingBagItemsCount, setShoppingBagItemsCount] = useState(0);
    const [shoppingBagTotalPrice, setShoppingBagTotalPrice] = useState(0);
    const [shoppingBagItems, setShoppingBagItems] = useState([]);

    useEffect(() => {
        let mounted = true;

        const loadShoppingBag = async () => {
            if (!userId) {
                setShoppingBagItems([]);
                setShoppingBagItemsCount(0);
                setShoppingBagTotalPrice(0);
                setLoading(false);
                return;
            }

            setLoading(true);

            try {
                const [itemsResponse, countResponse, priceResponse] =
                    await Promise.all([
                        getItems(),
                        getCount(),
                        getTotalPrice(),
                    ]);

                if (mounted) {
                    setShoppingBagItems(itemsResponse);
                    setShoppingBagItemsCount(countResponse.count);

                    const price =
                        typeof priceResponse.totalPrice === "string"
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
    }, [userId, getItems, getCount, getTotalPrice]);

    const deleteShoppingBagHandler = useCallback(
        async (id) => {
            setIsDeleting(true);

            const deletedItem = shoppingBagItems.find((item) => item.id === id);

            if (!deletedItem) {
                setIsDeleting(false);
                return;
            }

            try {
                await deleteItem(id);

                const updatedItems = shoppingBagItems.filter(
                    (item) => item.id !== id,
                );
                setShoppingBagItems(updatedItems);

                const newCount = Math.max(
                    0,
                    shoppingBagItemsCount - deletedItem.quantity,
                );
                setShoppingBagItemsCount(newCount);

                setShoppingBagTotalPrice((prev) => {
                    const currentPrice =
                        typeof prev === "string" ? parseFloat(prev) : prev;
                    const itemPrice =
                        typeof deletedItem.totalPrice === "string"
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
                            typeof priceResponse.totalPrice === "string"
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
        ],
    );

    const createShoppingBagItemHandler = useCallback(
        async (inventory) => {
            try {
                await createItem(inventory);

                const [itemsResponse, countResponse, priceResponse] =
                    await Promise.all([
                        getItems(),
                        getCount(),
                        getTotalPrice(),
                    ]);

                setShoppingBagItems(itemsResponse);
                setShoppingBagItemsCount(countResponse.count);

                const price =
                    typeof priceResponse.totalPrice === "string"
                        ? parseFloat(priceResponse.totalPrice)
                        : priceResponse.totalPrice;
                setShoppingBagTotalPrice(isNaN(price) ? 0 : price);

                return { success: true };
            } catch (error) {
                return { success: false, error };
            }
        },
        [createItem, getItems, getCount, getTotalPrice],
    );

    const continueCheckoutHandler = useCallback(() => {
        navigate("/user/checkout");
    }, [navigate]);

    const refreshShoppingBag = useCallback(async () => {
        try {
            const [itemsResponse, countResponse, priceResponse] =
                await Promise.all([getItems(), getCount(), getTotalPrice()]);

            setShoppingBagItems(itemsResponse);
            setShoppingBagItemsCount(countResponse.count);

            const price =
                typeof priceResponse.totalPrice === "string"
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
        ],
    );

    return (
        <ShoppingBagContext.Provider value={contextValue}>
            {children}
        </ShoppingBagContext.Provider>
    );
};
