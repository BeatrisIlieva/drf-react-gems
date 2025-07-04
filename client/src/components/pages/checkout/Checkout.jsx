import { useState, useTransition } from 'react';
import { Button } from '../../reusable/button/Button';
import { ComplimentaryShipping } from '../../reusable/complimentary-shipping/ComplimentaryShipping';
import { OrderSummary } from '../../reusable/order-summary/OrderSummary';
import { ShoppingBagSummaryList } from '../../reusable/shopping-bag-summary-list/ShoppingBagSummaryList';
import { DeliveryAddressForm } from '../accounts/details/delivery-address-form/DeliveryAddressForm';
import styles from './Checkout.module.scss';
import { ShadowBox } from '../../reusable/shadow-box/ShadowBox';

export const Checkout = () => {
    const [submitAction, setSubmitAction] = useState(null);
    const [isPending, startTransition] = useTransition();

    const handleFormReady = ({ submitAction }) => {
        setSubmitAction(() => submitAction);
    };

    const handleCheckoutSubmit = () => {
        if (submitAction) {
            startTransition(() => {
                submitAction();
            });
        }
    };

    return (
        <section className={styles['checkout']}>
            <div className={styles['wrapper-left']}>
                <DeliveryAddressForm
                    buttonTitle='Continue Checkout'
                    buttonGrow='1'
                    showButton={false}
                    onFormReady={handleFormReady}
                />
                <ShoppingBagSummaryList />
                <div
                    className={
                        styles['checkout-button-container']
                    }
                >
                    <ShadowBox>
                        <Button
                            title='Continue Checkout'
                            color='black'
                            actionType='button'
                            pending={isPending}
                            callbackHandler={handleCheckoutSubmit}
                            buttonGrow='1'
                        />
                    </ShadowBox>
                </div>
            </div>

            <OrderSummary separate={true}>
                <ComplimentaryShipping />
            </OrderSummary>
        </section>
    );
};
