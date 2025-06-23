import React from 'react';
import styles from './OrderSummary.module.scss';
import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';
import { Button } from '../button/Button';
import { ComplimentaryShipping } from '../complimentary-shipping/ComplimentaryShipping';
import { getTextRows } from './utils';
import { FlexTextRow } from '../flex-text-row/FlexTextRow';

export const OrderSummary: React.FC = () => {
    const { shoppingBagTotalPrice } = useShoppingBagContext();
    const textRows = getTextRows(shoppingBagTotalPrice);

    return (
        <section className={styles['order-summary']}>
            <h3>Order Summary</h3>

            <div>
                {textRows.map((row, index) => (
                    <FlexTextRow key={index} {...row} />
                ))}
            </div>

            <Button
                title={'Continue Checkout'}
                color={'black'}
                actionType={'button'}
                callbackHandler={() =>
                    console.log('Checkout clicked')
                }
            />

            <ComplimentaryShipping />
        </section>
    );
};
