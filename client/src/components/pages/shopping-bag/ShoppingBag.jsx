import { useEffect } from 'react';
import styles from './ShoppingBag.module.scss';
import { Delivery } from '../../reusable/delivery/Delivery';
import { OrderSummary } from '../../reusable/order-summary/OrderSummary';
import { ShoppingBagList } from './shopping-bag-list/ShoppingBagList';
import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';
import { EmptyList } from '../../reusable/empty-list/EmptyList';
import { Button } from '../../reusable/button/Button';
import { ComplimentaryShipping } from '../../reusable/complimentary-shipping/ComplimentaryShipping';
import { PaddedContainer } from '../../reusable/padded-container/PaddedContainer';
import { LoadingSpinner } from '../accounts/details/loading-spinner/LoadingSpinner';

export const ShoppingBag = () => {
    const {
        shoppingBagItems,
        getShoppingBagItemsHandler,
        continueCheckoutHandler
    } = useShoppingBagContext();

    const isEmpty =
        !shoppingBagItems || shoppingBagItems.length === 0;

    // Initial data load
    useEffect(() => {
        getShoppingBagItemsHandler();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    // Remove the conflicting useEffect that was overriding optimistic updates

    return (
        <PaddedContainer backgroundColor='white'>
            <section className={styles['shopping-bag']}>
                <h2>Shopping Bag</h2>

                {isEmpty ? (
                    <EmptyList title='shopping bag' />
                ) : (
                    <div className={styles['wrapper']}>
                        <div className={styles['wrapper-left']}>
                            <Delivery fontSize={1.4} />
                            <ShoppingBagList />
                        </div>

                        <OrderSummary>
                            <Button
                                title={'Continue Checkout'}
                                color={'black'}
                                actionType={'button'}
                                callbackHandler={
                                    continueCheckoutHandler
                                }
                                buttonGrow='1'
                            />

                            <ComplimentaryShipping />
                        </OrderSummary>
                    </div>
                )}
            </section>
        </PaddedContainer>
    );
};
