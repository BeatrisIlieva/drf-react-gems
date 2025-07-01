import { createContext, useContext } from 'react';

export const ShoppingBagContext = createContext({
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
