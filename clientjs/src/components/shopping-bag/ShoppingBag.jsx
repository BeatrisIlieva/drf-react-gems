import styles from './ShoppingBag.module.css';
import { OrderSummary } from '../reusable/order-summary/OrderSummary';
import { Delivery } from '../reusable/delivery/Delivery';
import { ShoppingBagList } from './shopping-bag-list/ShoppingBagList';

export const ShoppingBag = () => {
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
