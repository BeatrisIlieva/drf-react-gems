import { createContext, useContext } from 'react';

// Define types for the context value
export interface ShoppingBagItem {
    id: number;
    // Add other properties of shopping bag items here
    // For example: product_id: number, quantity: number, etc.
}

export interface ShoppingBagContextType {
    shoppingBagItems: ShoppingBagItem[];
    shoppingBagItemsCount: number;
    getShoppingBagItemsHandler: () => void;
    updateShoppingBagCount: () => void;
    shoppingBagTotalPrice: number;
}

export const ShoppingBagContext =
    createContext<ShoppingBagContextType>({
        shoppingBagItems: [],
        shoppingBagItemsCount: 0,
        getShoppingBagItemsHandler: () => null,
        updateShoppingBagCount: () => null,
        shoppingBagTotalPrice: 0
    });

export const useShoppingBagContext = () => {
    const data = useContext(ShoppingBagContext);

    return data;
};
