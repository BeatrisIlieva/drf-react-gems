import React from 'react';
import styles from './OrderSummary.module.scss';
import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';
import { getTextRows } from './utils';
import { FlexTextRow } from '../flex-text-row/FlexTextRow';
import { Skeleton } from './skeleton/Skeleton';

export const OrderSummary: React.FC = () => {
    const { shoppingBagTotalPrice, isLoading } =
        useShoppingBagContext();

    const textRows = React.useMemo(
        () => getTextRows(shoppingBagTotalPrice),
        [shoppingBagTotalPrice]
    );

    return (
        <section className={styles['order-summary']}>
            {isLoading ? (
                <Skeleton />
            ) : (
                <>
                    <h3>Order Summary</h3>

                    <div>
                        {textRows.map((row, index) => (
                            <FlexTextRow key={index} {...row} />
                        ))}
                    </div>
                </>
            )}
        </section>
    );
};
