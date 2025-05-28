import { useEffect } from 'react';
import { useShoppingBagContext } from '../../contexts/ShoppingBagContext';
import styles from './ShoppingBag.module.css';
import { OrderSummary } from '../reusable/order-summary/OrderSummary';

export const ShoppingBag = () => {
    const { shoppingBagItems, getShoppingBagItemsHandler } =
        useShoppingBagContext();

    useEffect(() => {
        getShoppingBagItemsHandler();
    }, [getShoppingBagItemsHandler]);

    console.log(shoppingBagItems);

    return (
        <section className={styles['shopping-bag']}>
            <h2>Shopping Bag</h2>
            <div className={styles['wrapper-left']}>here</div>

            <div className={styles['wrapper-right']}>
                <OrderSummary />
            </div>
        </section>
    );
};
