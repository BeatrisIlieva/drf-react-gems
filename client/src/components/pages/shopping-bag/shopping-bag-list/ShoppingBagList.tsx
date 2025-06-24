import { useEffect, type ReactElement } from 'react';
import { useShoppingBagContext } from '../../../../contexts/ShoppingBagContext';
import styles from './ShoppingBagList.module.scss';
import { ShoppingBagItem } from './shopping-bag-item/ShoppingBagItem';
import { Skeleton } from './skeleton/Skeleton';

export const ShoppingBagList = (): ReactElement => {
    const {
        shoppingBagItems,
        getShoppingBagItemsHandler,
        updateShoppingBagCount,
        updateShoppingBagTotalPrice,
        isLoading
    } = useShoppingBagContext();

    useEffect(() => {
        getShoppingBagItemsHandler();
        updateShoppingBagCount();
        updateShoppingBagTotalPrice();
    }, [
        updateShoppingBagCount,
        updateShoppingBagTotalPrice,
        getShoppingBagItemsHandler
    ]);

    if (
        isLoading &&
        (!shoppingBagItems || shoppingBagItems.length === 0)
    ) {
        return <Skeleton />;
    }

    return (
        <ul className={styles['shopping-bag-list']}>
            {shoppingBagItems.map((item) => (
                <ShoppingBagItem key={item.id} {...item} />
            ))}
        </ul>
    );
};
