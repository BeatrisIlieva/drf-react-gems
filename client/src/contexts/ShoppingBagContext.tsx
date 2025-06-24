import { createContext, useContext } from 'react';
import type { ShoppingBagItemResponse } from '../types/ShoppingBag';

export interface ShoppingBagContextType {
    shoppingBagItems: ShoppingBagItemResponse[];
    shoppingBagItemsCount: number;
    getShoppingBagItemsHandler: () => void;
    updateShoppingBagCount: () => void;
    shoppingBagTotalPrice: number;
    deleteShoppingBagHandler: (id: number) => void;
    isDeleting: boolean;
    isLoading: boolean;
    updateShoppingBagTotalPrice: () => void;
    continueCheckoutHandler: () => void;
}

export const ShoppingBagContext =
    createContext<ShoppingBagContextType>({
        shoppingBagItems: [],
        shoppingBagItemsCount: 0,
        getShoppingBagItemsHandler: () => null,
        updateShoppingBagCount: () => null,
        shoppingBagTotalPrice: 0,
        deleteShoppingBagHandler: () => null,
        isDeleting: false,
        isLoading: false,
        updateShoppingBagTotalPrice: () => null,
        continueCheckoutHandler: () => null
    });

export const useShoppingBagContext = () => {
    const data = useContext(ShoppingBagContext);

    return data;
};
