import { type ReactElement } from 'react';
import styles from './ShoppingBag.module.scss';
import { Delivery } from '../../reusable/delivery/Delivery';
import { OrderSummary } from '../../reusable/order-summary/OrderSummary';
import { ShoppingBagList } from './shopping-bag-list/ShoppingBagList';

export const ShoppingBag = (): ReactElement => {
    return (
        <section className={styles['shopping-bag']}>
            <h2>Shopping Bag</h2>
            <div className={styles['wrapper-left']}>
                <Delivery fontSize={'large'} />

                <ShoppingBagList />
            </div>

            <div className={styles['wrapper-right']}>
                <OrderSummary />
            </div>
        </section>
    );
};
