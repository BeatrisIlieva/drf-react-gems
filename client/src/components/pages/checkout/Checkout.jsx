import {
    useCallback,
    useState,
    useTransition,
    useEffect
} from 'react';
import { Button } from '../../reusable/button/Button';
import { ComplimentaryShipping } from '../../reusable/complimentary-shipping/ComplimentaryShipping';
import { OrderSummary } from '../../reusable/order-summary/OrderSummary';
import { DeliveryAddressForm } from '../accounts/details/delivery-address-form/DeliveryAddressForm';
import styles from './Checkout.module.scss';
import { ShadowBox } from '../../reusable/shadow-box/ShadowBox';
import { useNavigate } from 'react-router';
import { PaddedContainer } from '../../reusable/padded-container/PaddedContainer';
import { ProductsSummaryList } from '../../reusable/products-summary-list/ProductsSummaryList';
import { Delivery } from '../../reusable/delivery/Delivery';
import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';

export const Checkout = () => {
    const [submitAction, setSubmitAction] = useState(null);
    const [formState, setFormState] = useState(null);
    const [isPending, startTransition] = useTransition();
    const navigate = useNavigate();
    const { shoppingBagItems } = useShoppingBagContext();

    const handleFormReady = ({ submitAction, formState }) => {
        setSubmitAction(() => submitAction);
        setFormState(formState);
    };

    const continueCheckoutHandler = useCallback(() => {
        if (submitAction) {
            startTransition(() => {
                submitAction();
            });
        }
    }, [submitAction, startTransition]);

    useEffect(() => {
        if (formState?.success) {
            navigate('/user/payment');
        }
    }, [formState, navigate]);

    return (
        <PaddedContainer backgroundColor='lightest-grey'>
            <section className={styles['checkout']}>
                <div className={styles['wrapper-left']}>
                    <DeliveryAddressForm
                        buttonTitle='Continue Checkout'
                        buttonGrow='1'
                        showButton={false}
                        onFormReady={handleFormReady}
                    />
                    <ShadowBox>
                        <ProductsSummaryList
                            products={shoppingBagItems}
                        >
                            <Delivery fontSize={1.2} />
                        </ProductsSummaryList>
                    </ShadowBox>
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
                                callbackHandler={
                                    continueCheckoutHandler
                                }
                                buttonGrow='1'
                            />
                        </ShadowBox>
                    </div>
                </div>

                <OrderSummary separate={true}>
                    <ComplimentaryShipping />
                </OrderSummary>
            </section>
        </PaddedContainer>
    );
};
