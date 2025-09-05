import { useEffect, useState } from 'react';

import { useNavigate } from 'react-router';

import { CheckoutHeader } from '../../common/checkout-header/CheckoutHeader';
import { ComplimentaryShipping } from '../../reusable/complimentary-shipping/ComplimentaryShipping';
import { Delivery } from '../../reusable/delivery/Delivery';
import { OrderSummary } from '../../reusable/order-summary/OrderSummary';
import { PaddedContainer } from '../../reusable/padded-container/PaddedContainer';
import { ProductsSummaryList } from '../../reusable/products-summary-list/ProductsSummaryList';
import { ReturnPolicy } from '../../reusable/return-policy/ReturnPolicy';
import { ShadowBox } from '../../reusable/shadow-box/ShadowBox';
import { DeliveryAddressForm } from '../accounts/details/delivery-address-form/DeliveryAddressForm';

import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';

import styles from './Checkout.module.scss';

export const Checkout = () => {
    const navigate = useNavigate();
    const { shoppingBagItems } = useShoppingBagContext();

    const [formState, setFormState] = useState(null);

    const handleFormReady = ({ formState }) => {
        setFormState(formState);
    };

    useEffect(() => {
        if (formState?.success) {
            navigate('/user/payment');
        }
    }, [formState, navigate]);

    return (
        <PaddedContainer backgroundColor="lightest-grey">
            <CheckoutHeader />
            <section className={styles['checkout']}>
                <div className={styles['wrapper-left']}>
                    <ShadowBox>
                        <ProductsSummaryList products={shoppingBagItems}>
                            <Delivery fontSize={1.2} />
                        </ProductsSummaryList>
                    </ShadowBox>

                    <DeliveryAddressForm
                        buttonTitle="Continue Checkout"
                        buttonGrow="1"
                        onFormReady={handleFormReady}
                    />
                </div>

                <OrderSummary separate={true}>
                    <ComplimentaryShipping />
                    <ReturnPolicy />
                </OrderSummary>
            </section>
        </PaddedContainer>
    );
};
