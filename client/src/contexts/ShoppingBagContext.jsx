import { createContext, useContext } from 'react';

export const ShoppingBagContext = createContext({
    shoppingBagItems: [],
    shoppingBagItemsCount: 0,
    shoppingBagTotalPrice: 0,
    deleteShoppingBagHandler: () => null,
    isDeleting: false,
    loading: false,
    continueCheckoutHandler: () => null,
    refreshShoppingBag: () => null,
    createShoppingBagItemHandler: () => null,
});

export const useShoppingBagContext = () => {
    const data = useContext(ShoppingBagContext);

    return data;
};
