import { useEffect } from 'react';
import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';
import styles from './ShoppingBagList.module.css';
import { ShoppingBagItem } from './shopping-bag-item/ShoppingBagItem';

export const ShoppingBagList = () => {
    const { shoppingBagItems, getShoppingBagItemsHandler } =
        useShoppingBagContext();

    useEffect(() => {
        getShoppingBagItemsHandler();
    }, [getShoppingBagItemsHandler]);

    console.log(shoppingBagItems);

    return (
        <ul className={styles['shopping-bag-list']}>
            {shoppingBagItems.map((item) => (
                <ShoppingBagItem key={item.id} {...item} />
            ))}
        </ul>
    );
};
