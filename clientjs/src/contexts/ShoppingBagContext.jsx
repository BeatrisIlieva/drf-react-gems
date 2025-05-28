import {
    useContext,
    createContext,
    useEffect,
    useState,
    useCallback
} from 'react';
import { useGetShoppingBagItems } from '../api/useShoppingBagApi';

const ShoppingBagContext = createContext();

export const useShoppingBagContext = () => useContext(ShoppingBagContext);

export const ShoppingBagProvider = ({ children }) => {
    const { getShoppingBagItems } = useGetShoppingBagItems();
    const [shoppingBagItemsCount, setShoppingBagItemsCount] = useState(0);

    const [shoppingBagItems, setShoppingBagItems] = useState([]);

    const getShoppingBagItemsHandler = () => {
        getShoppingBagItems()
            .then((response) => {
                setShoppingBagItems(response);
                setShoppingBagItemsCount(response.length);
            })
            .catch((err) => console.log(err.message));
    }

    const getShoppingBagItemsCountHandler = () => { 
        setShoppingBagItemsCount(response.length);
    }

    useEffect(() => {
        getShoppingBagItems()
            .then((response) => {
                setShoppingBagItems(response);
                setShoppingBagItemsCount(response.length);
            })
            .catch((err) => console.log(err.message));
    }, [getShoppingBagItems, setShoppingBagItemsCount]);

    return (
        <ShoppingBagContext.Provider
            value={{ shoppingBagItems, shoppingBagItemsCount }}
        >
            {children}
        </ShoppingBagContext.Provider>
    );
};
