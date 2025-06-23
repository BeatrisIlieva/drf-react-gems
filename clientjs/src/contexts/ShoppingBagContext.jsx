import {
    useContext,
    createContext,
    useEffect,
    useState,
    useCallback
} from 'react';
import {
    useGetShoppingBagItems,
    useGetShoppingBagTotalPrice
} from '../api/useShoppingBagApi';
import { useGetShoppingBagCount } from '../api/useShoppingBagApi';

const ShoppingBagContext = createContext();

export const useShoppingBagContext = () => useContext(ShoppingBagContext);

export const ShoppingBagProvider = ({ children }) => {
    const { getShoppingBagItems } = useGetShoppingBagItems();
    const { getShoppingBagCount } = useGetShoppingBagCount();
    const { getShoppingBagTotalPrice } = useGetShoppingBagTotalPrice();

    const [shoppingBagItemsCount, setShoppingBagItemsCount] = useState(0);
    const [shoppingBagTotalPrice, setShoppingBagTotalPrice] = useState(0);

    const [shoppingBagItems, setShoppingBagItems] = useState([]);

    const getShoppingBagItemsHandler = useCallback(() => {
        getShoppingBagItems()
            .then((response) => {
                setShoppingBagItems(response);
                console.log(response, 'here');
            })
            .catch((err) => console.log(err.message));
    }, [getShoppingBagItems]);

    const updateShoppingBagCount = useCallback(() => {
        getShoppingBagCount()
            .then((response) => {
                setShoppingBagItemsCount(response.count);
            })
            .catch((err) => console.log(err.message));
    }, [getShoppingBagCount]);

    const updateShoppingBagTotalPrice = useCallback(() => {
        getShoppingBagTotalPrice()
            .then((response) => {
                setShoppingBagTotalPrice(response.total_price);
            })
            .catch((err) => console.log(err.message));
    }, [getShoppingBagTotalPrice]);

    useEffect(() => {
        updateShoppingBagCount();
        updateShoppingBagTotalPrice();
    }, [updateShoppingBagCount, updateShoppingBagTotalPrice]);

    return (
        <ShoppingBagContext.Provider
            value={{
                shoppingBagItems,
                shoppingBagItemsCount,
                getShoppingBagItemsHandler,
                updateShoppingBagCount,
                shoppingBagTotalPrice
            }}
        >
            {children}
        </ShoppingBagContext.Provider>
    );
};
