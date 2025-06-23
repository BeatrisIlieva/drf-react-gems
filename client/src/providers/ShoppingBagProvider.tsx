import {
    useCallback,
    useEffect,
    useState,
    type ReactNode
} from 'react';
import {
    useGetShoppingBagCount,
    useGetShoppingBagItems,
    useGetShoppingBagTotalPrice
} from '../api/shoppingBagApi';
import {
    ShoppingBagContext,
    type ShoppingBagContextType,
    type ShoppingBagItem
} from '../contexts/ShoppingBagContext';

export interface CountResponse {
    count: number;
}

export interface TotalPriceResponse {
    total_price: number;
}

interface Props {
    children: ReactNode;
}

export const ShoppingBagProvider = ({ children }: Props) => {
    const { getShoppingBagItems } = useGetShoppingBagItems();
    const { getShoppingBagCount } = useGetShoppingBagCount();
    const { getShoppingBagTotalPrice } =
        useGetShoppingBagTotalPrice();

    const [shoppingBagItemsCount, setShoppingBagItemsCount] =
        useState<number>(0);
    const [shoppingBagTotalPrice, setShoppingBagTotalPrice] =
        useState<number>(0);
    const [shoppingBagItems, setShoppingBagItems] = useState<
        ShoppingBagItem[]
    >([]);

    const getShoppingBagItemsHandler = useCallback(() => {
        getShoppingBagItems()
            .then((response) => {
                if (response) {
                    setShoppingBagItems(
                        response as unknown as ShoppingBagItem[]
                    );
                    console.log(response, 'here');
                }
            })
            .catch((err: Error) => console.log(err.message));
    }, [getShoppingBagItems]);

    const updateShoppingBagCount = useCallback(() => {
        getShoppingBagCount()
            .then((response) => {
                if (response) {
                    setShoppingBagItemsCount(
                        (response as unknown as CountResponse)
                            .count
                    );
                }
            })
            .catch((err: Error) => console.log(err.message));
    }, [getShoppingBagCount]);

    const updateShoppingBagTotalPrice = useCallback(() => {
        getShoppingBagTotalPrice()
            .then((response) => {
                if (response) {
                    setShoppingBagTotalPrice(
                        (
                            response as unknown as TotalPriceResponse
                        ).total_price
                    );
                }
            })
            .catch((err: Error) => console.log(err.message));
    }, [getShoppingBagTotalPrice]);

    useEffect(() => {
        updateShoppingBagCount();
        updateShoppingBagTotalPrice();
    }, [updateShoppingBagCount, updateShoppingBagTotalPrice]);

    const contextValue: ShoppingBagContextType = {
        shoppingBagItems,
        shoppingBagItemsCount,
        getShoppingBagItemsHandler,
        updateShoppingBagCount,
        shoppingBagTotalPrice
    };

    return (
        <ShoppingBagContext.Provider value={contextValue}>
            {children}
        </ShoppingBagContext.Provider>
    );
};

export default ShoppingBagProvider;
