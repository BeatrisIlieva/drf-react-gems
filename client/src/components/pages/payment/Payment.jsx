import { Delivery } from '../../reusable/delivery/Delivery';
import { OrderSummary } from '../../reusable/order-summary/OrderSummary';
import { PaddedContainer } from '../../reusable/padded-container/PaddedContainer';
import { ProductsSummaryList } from '../../reusable/products-summary-list/ProductsSummaryList';
import { PaymentForm } from './payment-form/PaymentForm';
import { ShippingInformation } from './shipping-information/ShippingInformation';

import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';

import styles from './Payment.module.scss';

export const Payment = () => {
    const { shoppingBagItems } = useShoppingBagContext();

    return (
        <PaddedContainer backgroundColor="lightest-grey">
            <section className={styles['checkout']}>
                <div className={styles['wrapper-left']}>
                    <ShippingInformation />
                    <PaymentForm />
                </div>

                <OrderSummary>
                    <ProductsSummaryList products={shoppingBagItems}>
                        <Delivery fontSize={1} />
                    </ProductsSummaryList>
                </OrderSummary>
            </section>
        </PaddedContainer>
    );
};
