import { useCallback, useState, type ReactNode } from 'react';
import {
    useDeleteShoppingBag,
    useGetShoppingBagCount,
    useGetShoppingBagItems,
    useGetShoppingBagTotalPrice
} from '../api/shoppingBagApi';
import {
    ShoppingBagContext,
    type ShoppingBagContextType
} from '../contexts/ShoppingBagContext';
import type { ShoppingBagItemResponse } from '../types/ShoppingBag';

export interface CountResponse {
    count: number;
}

export interface TotalPriceResponse {
    totalPrice: number;
}

interface Props {
    children: ReactNode;
}

export const ShoppingBagProvider = ({ children }: Props) => {
    const { getShoppingBagItems } = useGetShoppingBagItems();
    const { getShoppingBagCount } = useGetShoppingBagCount();
    const { getShoppingBagTotalPrice } =
        useGetShoppingBagTotalPrice();
    const { deleteShoppingBag } = useDeleteShoppingBag();
    const [isDeleting, setIsDeleting] = useState(false);

    const [shoppingBagItemsCount, setShoppingBagItemsCount] =
        useState<number>(0);
    const [shoppingBagTotalPrice, setShoppingBagTotalPrice] =
        useState<number>(0);
    const [shoppingBagItems, setShoppingBagItems] = useState<
        ShoppingBagItemResponse[]
    >([]);

    const getShoppingBagItemsHandler = useCallback(() => {
        getShoppingBagItems()
            .then((response) => {
                if (response) {
                    setShoppingBagItems(response);
                }
            })
            .catch((err: Error) => console.log(err.message));
    }, [getShoppingBagItems]);

    const updateShoppingBagCount = useCallback(() => {
        getShoppingBagCount()
            .then((response) => {
                if (response) {
                    setShoppingBagItemsCount(response.count);
                }
            })
            .catch((err: Error) => console.log(err.message));
    }, [getShoppingBagCount]);

    const updateShoppingBagTotalPrice = useCallback(() => {
        getShoppingBagTotalPrice()
            .then((response) => {
                if (response) {
                    setShoppingBagTotalPrice(response.totalPrice);
                }
            })
            .catch((err: Error) => console.log(err.message));
    }, [getShoppingBagTotalPrice]);

    const deleteShoppingBagHandler = async (id: number) => {
        setIsDeleting(true);
        try {
            await deleteShoppingBag(id);
            getShoppingBagItemsHandler();
            updateShoppingBagCount();
            updateShoppingBagTotalPrice();
        } catch (error) {
            console.error(error);
        }
        setIsDeleting(false);
    };

    const contextValue: ShoppingBagContextType = {
        shoppingBagItems,
        shoppingBagItemsCount,
        getShoppingBagItemsHandler,
        updateShoppingBagCount,
        shoppingBagTotalPrice,
        deleteShoppingBagHandler,
        isDeleting,
        updateShoppingBagTotalPrice
    };

    return (
        <ShoppingBagContext.Provider value={contextValue}>
            {children}
        </ShoppingBagContext.Provider>
    );
};

export default ShoppingBagProvider;
