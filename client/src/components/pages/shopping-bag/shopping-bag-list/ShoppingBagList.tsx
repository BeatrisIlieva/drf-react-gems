import React, { useEffect } from 'react';
import { useShoppingBagContext } from '../../../../contexts/ShoppingBagContext';
import styles from './ShoppingBagList.module.scss';
import { ShoppingBagItem } from './shopping-bag-item/ShoppingBagItem';
import type { ShoppingBagItemProps } from './shopping-bag-item/ShoppingBagItem';

export const ShoppingBagList: React.FC = () => {
    const { shoppingBagItems, getShoppingBagItemsHandler } =
        useShoppingBagContext();

    useEffect(() => {
        getShoppingBagItemsHandler();
    }, [getShoppingBagItemsHandler]);

    return (
        <ul className={styles['shopping-bag-list']}>
            {(shoppingBagItems as ShoppingBagItemProps[]).map(
                (item) => (
                    <ShoppingBagItem key={item.id} {...item} />
                )
            )}
        </ul>
    );
};
