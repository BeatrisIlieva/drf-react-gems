import { useEffect } from 'react';
import { useShoppingBagContext } from '../../../../contexts/ShoppingBagContext';
import styles from './ShoppingBagList.module.scss';
import { ShoppingBagItem } from './shopping-bag-item/ShoppingBagItem';
import { Skeleton } from './skeleton/Skeleton';
import { ShadowBox } from '../../../reusable/shadow-box/ShadowBox';

export const ShoppingBagList = () => {
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
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    if (
        isLoading &&
        (!shoppingBagItems || shoppingBagItems.length === 0)
    ) {
        return <Skeleton />;
    }

    return (
        <ShadowBox>
            <ul className={styles['shopping-bag-list']}>
                {shoppingBagItems.map((item) => (
                    <ShoppingBagItem key={item.id} {...item} />
                ))}
            </ul>
        </ShadowBox>
    );
};
