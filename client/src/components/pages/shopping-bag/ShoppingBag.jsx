import { useEffect,  } from 'react';
import styles from './ShoppingBag.module.scss';
import { Delivery } from '../../reusable/delivery/Delivery';
import { OrderSummary } from '../../reusable/order-summary/OrderSummary';
import { ShoppingBagList } from './shopping-bag-list/ShoppingBagList';
import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';
import { EmptyList } from '../../reusable/empty-list/EmptyList';
import { Button } from '../../reusable/button/Button';
import { ComplimentaryShipping } from '../../reusable/complimentary-shipping/ComplimentaryShipping';

export const ShoppingBag = () => {
    const {
        shoppingBagItems,
        getShoppingBagItemsHandler,
        updateShoppingBagCount,
        updateShoppingBagTotalPrice,
        continueCheckoutHandler
    } = useShoppingBagContext();

    const isEmpty =
        !shoppingBagItems || shoppingBagItems.length === 0;

    // Initial data load
    useEffect(() => {
        getShoppingBagItemsHandler();
    }, [getShoppingBagItemsHandler]);

    // Ensure count and price are always in sync with items
    useEffect(() => {
        // Update both count and total price when items change
        updateShoppingBagCount();
        updateShoppingBagTotalPrice();
    }, [
        shoppingBagItems.length,
        updateShoppingBagCount,
        updateShoppingBagTotalPrice
    ]);

    return (
        <section className={styles['shopping-bag']}>
            <h2>Shopping Bag</h2>

            {isEmpty ? (
                <EmptyList title='shopping bag' />
            ) : (
                <>
                    <div className={styles['wrapper-left']}>
                        <Delivery fontSize={'large'} />
                        <ShoppingBagList />
                    </div>

                    <div className={styles['wrapper-right']}>
                        <OrderSummary />
                        <Button
                            title={'Continue Checkout'}
                            color={'black'}
                            actionType={'button'}
                            callbackHandler={
                                continueCheckoutHandler
                            }
                        />

                        <ComplimentaryShipping />
                    </div>
                </>
            )}
        </section>
    );
};
