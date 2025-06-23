import { useEffect, type ReactElement } from 'react';
import { useShoppingBagContext } from '../../../../contexts/ShoppingBagContext';
import styles from './ShoppingBagList.module.scss';
import { ShoppingBagItem } from './shopping-bag-item/ShoppingBagItem';

export const ShoppingBagList = (): ReactElement => {
    const { shoppingBagItems, getShoppingBagItemsHandler } =
        useShoppingBagContext();

    useEffect(() => {
        getShoppingBagItemsHandler();
    }, [getShoppingBagItemsHandler]);

    return (
        <ul className={styles['shopping-bag-list']}>
            {shoppingBagItems.map((item) => (
                <ShoppingBagItem key={item.id} {...item} />
            ))}
        </ul>
    );
};
