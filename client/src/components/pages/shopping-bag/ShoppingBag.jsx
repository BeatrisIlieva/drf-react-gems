import { Button } from '../../reusable/button/Button';
import { ComplimentaryShipping } from '../../reusable/complimentary-shipping/ComplimentaryShipping';
import { Delivery } from '../../reusable/delivery/Delivery';
import { EmptyList } from '../../reusable/empty-list/EmptyList';
import { OrderSummary } from '../../reusable/order-summary/OrderSummary';
import { PaddedContainer } from '../../reusable/padded-container/PaddedContainer';
import { ShoppingBagList } from './shopping-bag-list/ShoppingBagList';

import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';

import styles from './ShoppingBag.module.scss';

export const ShoppingBag = () => {
    const { shoppingBagItems, continueCheckoutHandler } = useShoppingBagContext();

    return (
        <>
            {shoppingBagItems.length > 0 ? (
                <PaddedContainer backgroundColor="white">
                    <section className={styles['shopping-bag']}>
                        <h2>Shopping Bag</h2>
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
                                    callbackHandler={continueCheckoutHandler}
                                    buttonGrow="1"
                                />

                                <ComplimentaryShipping />
                            </OrderSummary>
                        </div>
                    </section>
                </PaddedContainer>
            ) : (
                <EmptyList title="Your Shopping bag is empty." />
            )}
        </>
    );
};
