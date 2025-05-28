import {
    useContext,
    createContext,
    useEffect,
    useState,
    useCallback
} from 'react';
import { useGetShoppingBagItems } from '../api/useShoppingBagApi';
import { useGetShoppingBagCount } from '../api/useShoppingBagApi';

const ShoppingBagContext = createContext();

export const useShoppingBagContext = () => useContext(ShoppingBagContext);

export const ShoppingBagProvider = ({ children }) => {
    const { getShoppingBagItems } = useGetShoppingBagItems();
    const { getShoppingBagCount } = useGetShoppingBagCount();
    const [shoppingBagItemsCount, setShoppingBagItemsCount] = useState(0);

    const [shoppingBagItems, setShoppingBagItems] = useState([]);

    const getShoppingBagItemsHandler = () => {
        getShoppingBagItems()
            .then((response) => {
                setShoppingBagItems(response);
            })
            .catch((err) => console.log(err.message));
    };

    useEffect(() => {
        getShoppingBagCount()
            .then((response) => {
                setShoppingBagItemsCount(response.count);
            })
            .catch((err) => console.log(err.message));
    }, [getShoppingBagCount]);

    return (
        <ShoppingBagContext.Provider
            value={{ shoppingBagItems, shoppingBagItemsCount, getShoppingBagItemsHandler }}
        >
            {children}
        </ShoppingBagContext.Provider>
    );
};
